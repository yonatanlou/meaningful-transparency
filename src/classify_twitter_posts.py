import re
import pandas as pd
import argparse
from dotenv import load_dotenv
from datetime import datetime
from constants import (
    DATA_DIR,
    LOGS_DIR,
    ANNOTATION_GLOB,
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    CLASSIFIER_SYSTEM_ALL_DEF,
    CLASSIFIER_SYSTEM_ONE_DEF,
    N_SAMPLES,
    MIN_CHARS,
    ANTISEMITISM_RATIO,
)
from utils import (
    load_definitions,
    setup_logger,
    truncate_text,
    generate_prompt,
    extract_pred_and_desc,
    get_answer,
    llm,
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Classify Twitter posts against antisemitism definitions"
    )
    parser.add_argument(
        "--model", default=MODEL, help=f"LLM model to use (default: {MODEL})"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=TEMPERATURE,
        help=f"Temperature for LLM (default: {TEMPERATURE})",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=N_SAMPLES,
        help=f"Number of samples to classify (default: {N_SAMPLES})",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=MIN_CHARS,
        help=f"Minimum character length for posts (default: {MIN_CHARS})",
    )
    parser.add_argument(
        "--results_filename",
        type=str,
        default="twitter_posts_classified",
        help="Base filename for results CSV (default: twitter_posts_classified)",
    )
    parser.add_argument(
        "--one-def",
        type=str,
        choices=["IHRA Definition", "Jerusalem Declaration", None],
        default=None,
        help="Use only one definition for classification (default: None - use all definitions)",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["train", "test", "original"],
        default="original",
        help="Dataset to use: train, test, or original (default: original)",
    )
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
    one_def = getattr(args, "one_def", None)
    dataset = args.dataset

    # Setup logging
    logger = setup_logger(
        str(LOGS_DIR / f"{results_filename}_{int(datetime.now().timestamp())}.log"),
        "llm_classifier",
    )

    # Load definitions and data
    all_annotations = load_definitions(str(ANNOTATION_GLOB))

    # Filter annotations based on --one-def argument
    if one_def:
        if one_def in all_annotations:
            annotations = {one_def: all_annotations[one_def]}
            system_prompt = CLASSIFIER_SYSTEM_ONE_DEF.replace(
                "<DEFINITION_NAME_PLACEHOLDER>", one_def
            )
        else:
            logger.error(
                f"Definition '{one_def}' not found in annotations. Available: {list(all_annotations.keys())}"
            )
            return
    else:
        annotations = all_annotations
        system_prompt = CLASSIFIER_SYSTEM_ALL_DEF

    # Choose dataset path based on argument
    if dataset == "train":
        dataset_path = DATA_DIR / "train_test_datasets" / "train.csv"
    elif dataset == "test":
        dataset_path = DATA_DIR / "train_test_datasets" / "test.csv"
    else:  # original
        raise NotImplementedError("Original dataset not implemented yet")

    twitter_df = pd.read_csv(str(dataset_path), encoding="cp1252", low_memory=False)

    # Log dataset info
    logger.info(
        "Loaded %s dataset: path=%s shape=%s columns=%s",
        dataset,
        dataset_path,
        twitter_df.shape,
        list(twitter_df.columns),
    )

    # Clean the text data
    twitter_df["Text"] = twitter_df["Text"].apply(
        lambda x: re.sub(r"@\w+", "", str(x)) if pd.notna(x) else x
    )
    twitter_df["Text"] = twitter_df["Text"].str.strip()
    twitter_df["text_length"] = twitter_df["Text"].apply(
        lambda x: len(str(x)) if pd.notna(x) else 0
    )

    samples = twitter_df[twitter_df["Text"].notna()].copy()
    samples = pd.concat(
        [
            samples[samples["Biased"] == 0].sample(
                int(n_samples * (1 - ANTISEMITISM_RATIO)), random_state=42
            ),
            samples[samples["Biased"] == 1].sample(
                int(n_samples * ANTISEMITISM_RATIO), random_state=42
            ),
        ]
    )
    logger.info(
        "Sampled %s rows with Biased=1 and text_length>%s", len(samples), min_chars
    )
    logger.info("Sampled rows indices: %s", samples.index.tolist())

    # Process all samples
    results_rows = []
    total_samples = len(samples)
    logger.info(
        "Using %s definition(s): %s",
        "single" if one_def else "all",
        list(annotations.keys()),
    )
    logger.info("System prompt: %s", system_prompt)
    logger.info("Starting to process %d samples", total_samples)

    for sample_num, (idx, row) in enumerate(samples.iterrows(), 1):
        # Extract fields
        text = str(row["Text"])
        biased = row["Biased"]
        keyword = (
            row["Keyword"] if "Keyword" in row and pd.notna(row["Keyword"]) else None
        )

        logger.info(
            "Sample %d/%d (Row %s): text=%s | keyword=%s",
            sample_num,
            total_samples,
            idx,
            truncate_text(text, 200),
            keyword,
        )

        prompt = generate_prompt(text, annotations)

        try:
            resp = llm(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                model,
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=MAX_TOKENS,
                return_json=True,
            )
        except Exception as e:
            logger.exception(
                "Sample %d/%d - llm() call failed on row %s: %s",
                sample_num,
                total_samples,
                idx,
                e,
            )
            results_rows.append(
                {
                    "original_index": idx,
                    "text": text,
                    "biased": biased,
                    "keyword": keyword,
                    "prediction": "LLM_ERROR",
                    "description": str(e),
                    "model": model,
                    "max_tokens": MAX_TOKENS,
                    "temperature": temperature,
                }
            )
            continue

        try:
            resp_text = get_answer(resp)
        except Exception as e:
            logger.exception(
                "Sample %d/%d - Failed extracting answer on row %s: %s",
                sample_num,
                total_samples,
                idx,
                e,
            )
            resp_text = '{"answer": "PARSING_ERROR", "description": "' + str(e) + '"}'

        logger.info("Raw model content (truncated): %s", truncate_text(resp_text, 800))

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
            "usage": resp.get("usage", {}),
        }
        logger.info(
            "Sample %d/%d - Result: prediction=%s",
            sample_num,
            total_samples,
            prediction,
        )

        results_rows.append(tmp_res)

    # Build results DataFrame
    results_df = pd.DataFrame(
        results_rows,
        columns=[
            "original_index",
            "text",
            "biased",
            "keyword",
            "prediction",
            "description",
            "model",
            "max_tokens",
            "temperature",
            "usage",
        ],
    )

    now = datetime.now().strftime("%Y-%m-%d-H:%H-M:%M")
    results_df.to_csv(f"outputs/{results_filename}_{now}.csv", index=False)

    logger.info(f"Finished. Results saved to outputs/{results_filename}_{now}.csv")


if __name__ == "__main__":
    main()
