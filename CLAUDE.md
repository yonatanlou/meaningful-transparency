# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an antisemitism classification system that uses LLMs to classify Twitter posts against different antisemitism definitions (IHRA Definition and Jerusalem Declaration). The main workflow involves loading Twitter posts, cleaning text, sampling based on bias ratios, and running classification through OpenRouter API.

## Essential Commands

**Setup and Installation:**
```bash
uv sync                    # Install all dependencies
cp .env-example .env       # Create environment file (add OPENROUTER_API_KEY)
```

**Main Classification Task:**
```bash
# Basic run with defaults
uv run python src/classify_twitter_posts.py

# With custom parameters
uv run python src/classify_twitter_posts.py --model anthropic/claude-sonnet-4 --temperature 0.1 --n-samples 100 --min-chars 50

# View available options
uv run python src/classify_twitter_posts.py --help
```

**Analysis and Reporting:**
```bash
uv run jupyter lab                    # Launch Jupyter for analysis
uv run jupyter nbconvert --to html notebooks/analysis.ipynb --output ../index.html
```

**Code Quality:**
```bash
uv run pre-commit run --all-files     # Run linting and formatting
uv run ruff check .                   # Manual linting
uv run ruff format .                  # Manual formatting
```

## Architecture

### Core Components

**Configuration System (`src/constants.py`):**
- Centralizes all paths, API settings, and LLM parameters
- Uses Path objects for cross-platform compatibility
- Contains the classification system prompt that defines the task

**Utilities (`src/utils.py`):**
- `load_definitions()`: Loads antisemitism definitions from markdown files in `prompts/annotation_guidelines/`
- `setup_logger()`: Creates dual logging (file + console) with rotation
- `llm()`: OpenRouter API wrapper with error handling and JSON response parsing
- Text processing utilities for prompt generation and response parsing

**Main Classification (`src/classify_twitter_posts.py`):**
- CLI-driven script with argparse
- Loads Twitter dataset from `datasets/GoldStanderDataSet.csv`
- Implements stratified sampling based on `ANTISEMITISM_RATIO` (70% antisemitic, 30% not)
- Processes each sample through LLM with structured JSON prompts
- Outputs timestamped CSV files to `outputs/` directory

### Data Flow

1. **Input**: Twitter posts from CSV with `Text`, `Biased`, and `Keyword` columns
2. **Sampling**: Stratified sampling based on text length and bias ratio
3. **Classification**: Each post sent to LLM with antisemitism definitions
4. **Output**: Results with predictions, descriptions, and usage metadata

### Key Configuration

**Sampling Strategy:**
- Uses `ANTISEMITISM_RATIO` (0.7) to maintain 70/30 split between biased/unbiased posts
- Filters posts by `MIN_CHARS` to ensure sufficient content
- Random state fixed at 42 for reproducibility

**LLM Integration:**
- Uses OpenRouter API supporting multiple model providers
- Structured JSON responses with schema validation
- Comprehensive error handling for API failures and parsing errors
- Token usage tracking for cost analysis

## Pre-commit Automation

The repository has automated pre-commit hooks that:
1. Run ruff linting and formatting on Python files
2. Execute `src/sh_scripts.sh` which regenerates `index.html` from analysis notebook
3. Automatically add the updated HTML to the commit

This ensures the analysis report is always current with notebook changes.

## Environment Requirements

- Python ≥3.12
- OpenRouter API key for LLM access
- Uses `uv` for dependency management
- Input data expected at `datasets/GoldStanderDataSet.csv`
- Antisemitism definitions as markdown files in `prompts/annotation_guidelines/`