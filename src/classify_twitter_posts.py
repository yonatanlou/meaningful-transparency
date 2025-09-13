import argparse
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from constants import (ANNOTATION_GLOB, ANTISEMITISM_RATIO,
                       CLASSIFIER_SYSTEM_ONE_DEF, DATA_DIR, LOGS_DIR,
                       MAX_TOKENS, MODEL, N_SAMPLES, TEMPERATURE)
from utils import (extract_pred_and_desc, get_answer, llm, load_definitions,
                   setup_logger, truncate_text)


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
        "--results_filename",
        type=str,
        default="twitter_posts_classified",
        help="Base filename for results CSV (default: twitter_posts_classified)",
    )
    parser.add_argument(
        "--one-def",
        type=str,
        choices=["IHRA Definition"],
        default="IHRA Definition",
        help="Use IHRA Definition for classification (only option available)",
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
    results_filename = args.results_filename
    one_def = getattr(args, "one_def", None)
    dataset = args.dataset

    # Setup logging
    log_path = LOGS_DIR / f"{results_filename}_{int(datetime.now().timestamp())}.log"

    # Create directory if it doesn't exist
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = setup_logger(
        str(log_path),
        "llm_classifier",
    )

    # Load definitions and data
    all_annotations = load_definitions(str(ANNOTATION_GLOB))

    # Use only IHRA Definition
    if one_def != "IHRA Definition":
        logger.error(f"Only 'IHRA Definition' is supported, got: {one_def}")
        raise ValueError("Only 'IHRA Definition' is supported")

    if one_def not in all_annotations:
        logger.error(
            f"Definition '{one_def}' not found in annotations. Available: {list(all_annotations.keys())}"
        )
        raise ValueError(f"Definition '{one_def}' not found")

    annotations = {one_def: all_annotations[one_def]}
    system_prompt = CLASSIFIER_SYSTEM_ONE_DEF.replace(
        "<DEFINITION_NAME_PLACEHOLDER>", one_def
    )

    # Choose dataset path based on argument
    if dataset == "train":
        dataset_path = DATA_DIR / "train_test_datasets" / "train.csv"
    elif dataset == "test":
        dataset_path = DATA_DIR / "train_test_datasets" / "test.csv"
    else:  # original
        raise NotImplementedError("Original dataset not implemented yet")

    twitter_df = pd.read_csv(str(dataset_path), low_memory=False)

    # Log dataset info
    logger.info(
        "Loaded %s dataset: path=%s shape=%s columns=%s",
        dataset,
        dataset_path,
        twitter_df.shape,
        list(twitter_df.columns),
    )

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
    logger.info("Sampled %s rows from dataset", len(samples))
    logger.info("Sampled rows indices: %s", samples.index.tolist())

    # Process all samples
    results_rows = []
    total_samples = len(samples)
    logger.info(
        "Using single definition: %s",
        list(annotations.keys())[0],
    )
    logger.info("System prompt: %s", system_prompt)
    annotation_guidelines = all_annotations[one_def]
    logger.info("User prompt template: %s", annotation_guidelines)

    logger.info("Starting to process %d samples", total_samples)

    for sample_num, (idx, row) in enumerate(samples.iterrows(), 1):
        # Extract fields
        text = str(row["cleaned_text"])
        biased = row["Biased"]
        keyword = (
            row["Keyword"] if "Keyword" in row and pd.notna(row["Keyword"]) else None
        )
        user_prompt = annotation_guidelines.replace("{{text}}", text)
        logger.info(
            "Sample %d/%d (Row %s): prompt[-200:]=%s | keyword=%s",
            sample_num,
            total_samples,
            idx,
            user_prompt[-200:],
            keyword,
        )

        

        try:
            resp = llm(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
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
    output_path = Path("outputs") / f"{results_filename}_{now}.csv"

    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(output_path, index=False)

    logger.info(f"Finished. Results saved to {output_path}")


if __name__ == "__main__":
    main()
