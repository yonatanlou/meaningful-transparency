import re
import pandas as pd
import argparse
from dotenv import load_dotenv
from datetime import datetime
from constants import (
    CSV_PATH, LOG_FILE, ANNOTATION_GLOB, MODEL, 
    TEMPERATURE, MAX_TOKENS, CLASSIFIER_SYSTEM, N_SAMPLES, MIN_CHARS, ANTISEMITISM_RATIO
)
from utils import (
    load_definitions, setup_logger, truncate_text, 
    generate_prompt, extract_pred_and_desc, get_answer, llm
)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Classify Twitter posts against antisemitism definitions")
    parser.add_argument("--model", default=MODEL, 
                       help=f"LLM model to use (default: {MODEL})")
    parser.add_argument("--temperature", type=float, default=TEMPERATURE,
                       help=f"Temperature for LLM (default: {TEMPERATURE})")
    parser.add_argument("--n-samples", type=int, default=N_SAMPLES,
                       help=f"Number of samples to classify (default: {N_SAMPLES})")
    parser.add_argument("--min-chars", type=int, default=MIN_CHARS,
                       help=f"Minimum character length for posts (default: {MIN_CHARS})")
    parser.add_argument("--results_filename", type=str, default="twitter_posts_classified",
                       help="Base filename for results CSV (default: twitter_posts_classified)")
    return parser.parse_args()

def main():
    load_dotenv()
    args = parse_args()
    
    # Use CLI args or defaults
    model = args.model
    temperature = args.temperature
    n_samples = args.n_samples
    min_chars = args.min_chars
    results_filename = args.results_filename
    
    # Setup logging
    logger = setup_logger(str(LOG_FILE), "llm_classifier")
    
    # Load definitions and data
    annotations = load_definitions(str(ANNOTATION_GLOB))
    twitter_df = pd.read_csv(str(CSV_PATH), encoding="cp1252", low_memory=False)

    # Log dataset info
    logger.info("Loaded CSV: path=%s shape=%s columns=%s",
                CSV_PATH, twitter_df.shape, list(twitter_df.columns))

    # Clean the text data 
    twitter_df['Text'] = twitter_df['Text'].apply(
        lambda x: re.sub(r'@\w+', '', str(x)) if pd.notna(x) else x
    )
    twitter_df['Text'] = twitter_df['Text'].str.strip()
    twitter_df['text_length'] = twitter_df['Text'].apply(
        lambda x: len(str(x)) if pd.notna(x) else 0
    )

    samples = twitter_df[twitter_df["Text"].notna()].copy()
    samples = samples[(samples["text_length"]>min_chars)]
    samples = pd.concat([
    samples[samples["Biased"]==0].sample(int(n_samples*(1-ANTISEMITISM_RATIO)), random_state=42),
    samples[samples["Biased"]==1].sample(int(n_samples*ANTISEMITISM_RATIO), random_state=42)
])
    logger.info("Sampled %s rows with Biased=1 and text_length>%s", len(samples), min_chars)
    logger.debug("Sampled rows indices: %s", samples.index.tolist())

    # Process all samples
    results_rows = []
    total_samples = len(samples)
    logger.info('System prompt for all prompts %s', CLASSIFIER_SYSTEM)
    logger.info('Starting to process %d samples', total_samples)

    for sample_num, (idx, row) in enumerate(samples.iterrows(), 1):
        # Extract fields
        text = str(row["Text"])
        biased = row["Biased"]
        keyword = row["Keyword"] if "Keyword" in row and pd.notna(row["Keyword"]) else None

        logger.info("Sample %d/%d (Row %s): text=%s | keyword=%s",
                    sample_num, total_samples, idx, truncate_text(text, 200), keyword)

        prompt = generate_prompt(text, annotations)
        logger.debug("Prompt (truncated): %s", truncate_text(prompt, 800))

        try:
            resp = llm(
                [
                    {"role": "system", "content": CLASSIFIER_SYSTEM},
                    {"role": "user", "content": prompt},
                ],
                model,
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=MAX_TOKENS,
                return_json=True,
            )
        except Exception as e:
            logger.exception("Sample %d/%d - llm() call failed on row %s: %s", sample_num, total_samples, idx, e)
            results_rows.append({
                "original_index": idx,
                "text": text,
                "biased": biased,
                "keyword": keyword,
                "prediction": "LLM_ERROR",
                "description": str(e),
                "model": model,
                "max_tokens": MAX_TOKENS,
                "temperature": temperature,
            })
            continue

        try:
            resp_text = get_answer(resp)
        except Exception as e:
            logger.exception("Sample %d/%d - Failed extracting answer on row %s: %s", sample_num, total_samples, idx, e)
            resp_text = '{"answer": "PARSING_ERROR", "description": "' + str(e) + '"}'

        logger.debug("Raw model content (truncated): %s", truncate_text(resp_text, 800))

        prediction, desc = extract_pred_and_desc(resp_text, annotations)

        tmp_res = {
            "original_index": idx,
            "text": text,
            "biased": biased,
            "keyword": keyword,
            "prediction": prediction,
            "description": desc,
            "model": model,
            "max_tokens": MAX_TOKENS,
            "temperature": temperature,
            "usage": resp.get("usage", {})
        }
        logger.info("Sample %d/%d - Result: prediction=%s", sample_num, total_samples, prediction)

        results_rows.append(tmp_res)

    # Build results DataFrame
    results_df = pd.DataFrame(
        results_rows,
        columns=["original_index", "text", "biased","keyword", "prediction", "description", "model", "max_tokens", "temperature", "usage"]
    )

    
    now = datetime.now().strftime("%Y-%m-%d-H:%H-M:%M")
    results_df.to_csv(f"outputs/{results_filename}_{now}.csv", index=False)
    
    logger.info("Finished. Results saved to outputs/twitter_posts_classified_%s.csv", now)


if __name__ == "__main__":
    main()