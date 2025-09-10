# Meaningful Transparency

A tool for classifying Twitter posts against different antisemitism definitions using LLMs.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Setup environment:**
   - Copy `.env-example` to `.env`
   - Add your OpenRouter API key

3. **Run classification:**
   ```bash
   uv run python src/classify_twitter_posts.py
   ```
   
   Or with custom parameters:
   ```bash
   uv run python src/classify_twitter_posts.py --model anthropic/claude-sonnet-4 --temperature 0 --n-samples 750 --min-chars 50 --results_filename small_test/twitter_posts_classified_IHRA --dataset train
   ```

## What it does

`src/classify_twitter_posts.py` is the main classification script that:

- Loads Twitter posts from train/test datasets or original data
- Samples posts using stratified sampling (70% antisemitic, 30% non-antisemitic)
- Uses LLM to classify each post against the IHRA Definition of antisemitism
- Outputs results to `outputs/twitter_posts_classified_{timestamp}.csv`

The script uses structured prompts to get JSON responses and logs all activities to `logs/llm_classifier.log`.

## Configuration

You can configure the script via CLI arguments or by editing `src/constants.py`:
- `--model`: LLM model to use (default: anthropic/claude-sonnet-4)
- `--temperature`: Temperature for LLM (default: 0)
- `--n-samples`: Number of posts to classify (default: 2)
- `--min-chars`: Minimum text length (default: 100)
- `--results_filename`: Base filename for results CSV (default: twitter_posts_classified)
- `--one-def`: Definition to use - only "IHRA Definition" is supported (default: IHRA Definition)
- `--dataset`: Dataset to use - train, test, or original (default: original)

## Output Format

Results include:
- `original_index`: Index from source dataset
- `text`: Cleaned post text  
- `biased`: Ground truth label (0/1)
- `keyword`: Associated keyword (Israel/Jews)
- `prediction`: True (antisemitic) or False (not antisemitic)
- `description`: LLM's reasoning
- `usage`: Token usage information
- Metadata: model, temperature, max_tokens
