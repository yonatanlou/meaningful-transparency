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
   uv run python src/classify_twitter_posts.py --model openai/gpt-4o --temperature 0.2 --n-samples 10 --min-chars 50 --results_filename twitter_posts_classified
   ```

## What it does

`src/classify_twitter_posts.py` is the main classification script that:

- Loads Twitter posts from `datasets/GoldStanderDataSet.csv`
- Samples posts with sufficient text length
- Uses LLM to classify each post against antisemitism definitions:
  - IHRA Definition
  - Jerusalem Declaration
- Outputs results to `outputs/twitter_posts_classified_{date}.csv`

The script uses structured prompts to get JSON responses and logs all activities to `logs/llm_classifier.log`.

## Configuration

You can configure the script via CLI arguments or by editing `src/constants.py`:
- `--model`: LLM model to use (default: openai/gpt-4o-mini)
- `--temperature`: Temperature for LLM (default: 0.1)
- `--n-samples`: Number of posts to classify (default: 2)
- `--min-chars`: Minimum text length (default: 100)

## Output Format

Results include:
- `original_index`: Index from source dataset
- `text`: Cleaned post text
- `prediction`: IHRA Definition or Jerusalem Declaration
- `description`: LLM's reasoning
- Metadata: model, temperature, max_tokens
