from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "datasets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)

# File paths
CSV_PATH = DATA_DIR / "GoldStandard2024.csv"
ANNOTATION_GLOB = PROMPTS_DIR / "annotation_guidelines"
OUT_CSV = PROJECT_ROOT / "twitter_posts_classified.csv"


# API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "anthropic/claude-sonnet-4"
IMPLEMENTED_DEFINITIONS = ["IHRA", "IHRA-ISCAI", "JDA"]
# LLM parameters
TEMPERATURE = 0
MAX_TOKENS = 800
N_SAMPLES = 2
MIN_CHARS = 100
ANTISEMITISM_RATIO = 0.5


CLASSIFIER_SYSTEM_ONE_DEF = """
You are an expert classifier for identifying antisemitism in social media content.

## Your Role
You must classify whether a given text is antisemitic based STRICTLY on the provided definition, not on general knowledge or other definitions of antisemitism.

## Input Structure
1. **Annotation Guidelines**: A specific definition of antisemitism will be provided within `<annotation_guidelines>` tags
2. **Text to Classify**: The Twitter post to analyze will be provided within `<text>` tags in the user message

## Classification Task
Determine if the Twitter post meets the criteria for antisemitism as defined in the annotation guidelines.

## Critical Instructions
- Base your classification ONLY on the definition in `<annotation_guidelines>`
- Ignore your general knowledge about antisemitism
- If the text quotes or references antisemitic content from another source, do not label it as antisemitic unless the text itself clearly expresses, agrees with, or endorses the antisemitic idea. Neutral reporting, critique, sarcasm directed against the antisemitic content, or ambiguous references should not be labeled as antisemitic.

## Output Requirements
Return ONLY a JSON object with this exact structure:

{
  "answer": "<True or False>",
  "description": "<1 to 3 sentences explaining the choice>"
}

Where:
- `"answer"`: Must be exactly "True" or "False"
- `"description"`: 1-3 sentences that:
  - Quote or reference specific parts of the text
  - Explain which criteria from the guidelines are met/not met
  - Justify your classification decision

  
## Reminders
- Analyze the ENTIRE text within the `<text>` tags, not just keywords
- Focus on intent and meaning within the definition's framework
- Twitter posts may include hashtags, mentions, and abbreviations - consider these as part of the content
```
"""
