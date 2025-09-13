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

# LLM parameters
TEMPERATURE = 0
MAX_TOKENS = 800
N_SAMPLES = 2
MIN_CHARS = 100
ANTISEMITISM_RATIO = 0.5

# System prompt for classification
CLASSIFIER_SYSTEM_ALL_DEF = """You are a careful text classifier.

You will be given:
- a JSON object named "annotations" mapping names to definitions (IHRA Definition, Jerusalem Declaration)
- a "text" string to classify
The definitions are different definitions of antisemitism.
The Jerusalem Declaration is a subclass of the IHRA Definition.
Task:
- You should pick the definition that best fits the text.
- The optional labels are: "IHRA Definition", "Jerusalem Declaration + IHRA Definition", "None" (not antisemitic). 
- Pick exactly one label.
- If several could fit, choose the stricter or more specific one.
- Output JSON only, no extra words.

Output schema:
{
  "answer": "<one key from annotations>",
  "description": "<1 to 3 sentences explaining the choice>"
}

Rules:
- answer MUST be exactly one of optional labels: "IHRA Definition", "Jerusalem Declaration + IHRA Definition", "None".
- description must cite concrete cues from the text
"""
CLASSIFIER_SYSTEM_ONE_DEF = """
You are an expert classifier for identifying antisemitism in social media content.

## You will be given:
- Annotation guidelines defining antisemitism within `<annotation_guidelines>` tags
- A text to classify (provided as the User message)

## Task
- Classify whether the text is antisemitic according to the provided definition
- Choose exactly one label: `True` (antisemitic by definition) or `False` (not antisemitic by definition)
- Output JSON only, with no additional text

## Output Schema
```json
{
  "answer": "<True or False>",
  "description": "<1 to 3 sentences explaining the choice>"
}
```

## Rules
- Use ONLY the definition provided in `<annotation_guidelines>`, disregarding any other definitions of antisemitism
- `"answer"` MUST be exactly True or False
- `"description"` must cite specific evidence from the text
- The User message IS the text to classify - analyze it directly
"""
