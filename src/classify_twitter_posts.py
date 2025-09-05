import re
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from constants import (
    CSV_PATH, LOG_FILE, ANNOTATION_GLOB, MODEL, 
    TEMPERATURE, MAX_TOKENS, CLASSIFIER_SYSTEM, N_SAMPLES, MIN_CHARS
)
from utils import (
    load_definitions, setup_logger, truncate_text, 
    generate_prompt, extract_pred_and_desc, get_answer, llm
)

load_dotenv()

# Setup logging
logger = setup_logger(str(LOG_FILE), "grok_classifier")

# Load definitions and data
annotations = load_definitions(str(ANNOTATION_GLOB))
twitter_df = pd.read_csv(str(CSV_PATH), encoding="cp1252", low_memory=False)

# Clean the text data
twitter_df['Text'] = twitter_df['Text'].apply(
    lambda x: re.sub(r'@\w+', '', str(x)) if pd.notna(x) else x
)
twitter_df['Text'] = twitter_df['Text'].str.strip()
twitter_df['text_length'] = twitter_df['Text'].apply(
    lambda x: len(str(x)) if pd.notna(x) else 0
)

# Log dataset info
logger.info("Loaded CSV: path=%s shape=%s columns=%s",
            CSV_PATH, twitter_df.shape, list(twitter_df.columns))


samples = twitter_df[twitter_df["Text"].notna()].copy()
samples = samples[(samples["Biased"] == 1) & (samples["text_length"]>MIN_CHARS)].sample(N_SAMPLES, random_state=42)
logger.info("Sampled %s rows with Biased=1 and text_length>%s", len(samples), MIN_CHARS)
logger.debug("Sampled rows indices: %s", samples.index.tolist())

# Process all samples
results_rows = []
logger.info('System prompt for all prompts %s', CLASSIFIER_SYSTEM)

for idx, row in samples.iterrows():
    # Extract fields
    text = str(row["Text"])
    keyword = row["Keyword"] if "Keyword" in row and pd.notna(row["Keyword"]) else None

    logger.info("Row %s: text=%s | keyword=%s",
                idx, truncate_text(text, 200), keyword)

    prompt = generate_prompt(text, annotations)
    logger.debug("Prompt (truncated): %s", truncate_text(prompt, 800))

    try:
        resp = llm(
            [
                {"role": "system", "content": CLASSIFIER_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            MODEL,
            response_format={"type": "json_object"},
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            return_json=True,
        )
    except Exception as e:
        logger.exception("llm() call failed on row %s: %s", idx, e)
        results_rows.append({
            "original_index": idx,
            "text": text,
            "keyword": keyword,
            "prediction": "LLM_ERROR",
            "description": str(e),
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        })
        continue

    try:
        resp_text = get_answer(resp)
    except Exception as e:
        logger.exception("Failed extracting answer on row %s: %s", idx, e)
        resp_text = '{"answer": "PARSING_ERROR", "description": "' + str(e) + '"}'

    logger.debug("Raw model content (truncated): %s", truncate_text(resp_text, 800))

    prediction, desc = extract_pred_and_desc(resp_text, annotations)

    log_row_preview = {
        "text": truncate_text(text, 160),
        "keyword": keyword,
        "prediction": prediction,
        "description": truncate_text(desc, 200),
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    logger.info("Result row: %s", log_row_preview)

    results_rows.append({
        "original_index": idx,
        "text": text,
        "keyword": keyword,
        "prediction": prediction,
        "description": desc,
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    })

# Build results DataFrame
results_df = pd.DataFrame(
    results_rows,
    columns=["original_index", "text", "keyword", "prediction", "description", "model", "max_tokens", "temperature"]
)

results_df.to_csv("twitter_posts_classified.csv", index=False, encoding="utf-8")
today = datetime.now().strftime("%Y-%m-%d")
results_df.to_csv(f"outputs/twitter_posts_classified_{today}.csv", index=False)