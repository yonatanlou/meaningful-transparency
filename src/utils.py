import os
import json
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from logging.handlers import RotatingFileHandler

from constants import OPENROUTER_BASE_URL

def load_definitions(definitions_dir: str) -> Dict[str, str]:
    """Load antisemitism definitions from markdown files."""
    definitions = {}
    definitions_path = Path(definitions_dir)
    
    if not definitions_path.exists():
        raise FileNotFoundError(f"Directory {definitions_dir} not found")
    
    for md_file in definitions_path.glob("*.md"):
        definition_name = md_file.stem
        with open(md_file, 'r', encoding='utf-8') as f:
            definitions[definition_name] = f.read().strip()
    
    if not definitions:
        raise RuntimeError("No definitions found")
    return definitions


def setup_logger(log_file: str, logger_name: str = "classifier") -> logging.Logger:
    """Setup logger with file rotation and console output."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers on repeated runs
    if logger.handlers:
        logger.handlers.clear()
    
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    
    return logger


def truncate_text(s: str | None, n: int = 1500) -> str:
    """Truncate text to specified length with ellipsis."""
    if not s:
        return ""
    return (s[:n] + "...") if len(s) > n else s


def generate_prompt(text: str, annotations: Dict[str, str]) -> str:
    """Generate the user prompt content for classification."""
    return (
        "annotations:\n"
        + json.dumps(annotations, ensure_ascii=False, indent=2)
        + "\n\ntext:\n"
        + text
        + "\n\nRespond with JSON only matching the schema."
    )


def extract_pred_and_desc(json_text: str, allowed_keys: Dict[str, str]) -> Tuple[str, str]:
    """Parse JSON and validate 'answer' against provided annotations keys."""
    try:
        obj = json.loads(json_text)
        answer = obj.get("answer", "")
        desc = obj.get("description", "")
        
        if not desc:
            desc = "Model answer not in annotation keys; fell back to the first key."
        return answer, desc
    except Exception:
        # If the model did not return JSON, store the raw text for debugging
        return json_text, json_text


def get_answer(resp):
    """Extract answer from OpenAI-style response."""
    return resp["choices"][0]["message"]["content"]



def _build_headers(
    api_key: Optional[str] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Compose required and optional headers."""
    key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    # Optional attribution headers (helpful for rankings/analytics)
    # https://openrouter.ai/docs/quickstart • https://openrouter.ai/docs/app-attribution
    site_url = os.getenv("OPENROUTER_SITE_URL")
    site_name = os.getenv("OPENROUTER_SITE_NAME")
    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_name:
        headers["X-Title"] = site_name

    if extra_headers:
        headers.update(extra_headers)

    return headers


def llm(
    messages: List[Dict[str, Any]],
    model: str,
    *,
    api_key: Optional[str] = None,
    base_url: str = OPENROUTER_BASE_URL,
    timeout: int = 90,
    extra_headers: Optional[Dict[str, str]] = None,
    return_json: bool = False,
    **kwargs: Any,
) -> Any:
    """
    Simple OpenRouter chat call.

    Required:
      - messages: OpenAI-style messages [{"role": "...", "content": "..."}]
      - model: e.g. "openai/gpt-4o-mini"

    Optional:
      - Any extra OpenAI Chat Completions fields via **kwargs, for example:
        temperature, max_tokens, top_p, stop, seed, response_format, tools, tool_choice

    Returns:
      - By default, the first message string
      - If return_json=True, the full parsed JSON response

    Docs: https://openrouter.ai/docs/api-reference/chat-completion
    """
    if not isinstance(messages, list):
        raise ValueError("messages must be a list of dicts")

    url = f"{base_url.rstrip('/')}/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
    }
    # Forward any supported parameters (temperature, max_tokens, etc.)
    payload.update({k: v for k, v in kwargs.items() if v is not None})

    headers = _build_headers(api_key=api_key, extra_headers=extra_headers)

    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    if not resp.ok:
        # Try to include server error details when possible
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {detail}")

    data = resp.json()
    if return_json:
        return data

    # Standard OpenAI-style shape
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected response shape: {json.dumps(data)[:500]}")


