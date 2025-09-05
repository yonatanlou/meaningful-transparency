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
   cd src && python classify_twitter_posts.py
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

Key settings in `src/constants.py`:
- `N_SAMPLES`: Number of posts to classify (default: 2)
- `MIN_CHARS`: Minimum text length (default: 100)
- `MODEL`: LLM model to use (default: openai/gpt-4o-mini)

## Output Format

Results include:
- `original_index`: Index from source dataset
- `text`: Cleaned post text
- `prediction`: IHRA Definition or Jerusalem Declaration
- `description`: LLM's reasoning
- Metadata: model, temperature, max_tokens
