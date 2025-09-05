# pip install openai requests
# For Google, you can use an API key for quick demos (?key=...), or OAuth service-account auth for prod.

import os
import requests
from typing import Dict
from dotenv import load_dotenv
from collections import OrderedDict

load_dotenv()  # take environment variables from .env file
# 1) OpenAI Moderation API
# Docs: omni-moderation-latest model and response fields
# https://platform.openai.com/docs/guides/moderation  | https://platform.openai.com/docs/models/omni-moderation-latest
from openai import OpenAI

def classify_with_openai(text: str) -> Dict[str, float]:
    """
    Returns {category: probability} using OpenAI Moderation.
    Requires: OPENAI_API_KEY env var.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.moderations.create(model="omni-moderation-latest", input=text)
    # Pull scores from the first result
    scores = dict(resp.results[0].category_scores)
    scores = OrderedDict(sorted(scores.items(), key=lambda item: item[1], reverse=True))  
    return {f"openai:{k}": float(v) for k, v in scores.items()}


# 2) Perspective API (Jigsaw)
# Docs: AnalyzeComment and attributeScores
# https://developers.perspectiveapi.com/s/docs-sample-requests?language=en_US
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Choose the attributes you care about. Add more if you like (e.g., SEXUALLY_EXPLICIT, FLIRTATION).
PERSPECTIVE_ATTRS = {
    "TOXICITY": {},
    "SEVERE_TOXICITY": {},
    "INSULT": {},
    "PROFANITY": {},
    "THREAT": {},
    "IDENTITY_ATTACK": {},
}


from googleapiclient import discovery
import json



def classify_with_perspective(text: str) -> Dict[str, float]:
    """
    Returns {category: probability} using Perspective API.
    Requires: PERSPECTIVE_API_KEY env var.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing PERSPECTIVE_API_KEY")

    client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=os.getenv("PERSPECTIVE_API_KEY"),
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
    )

    analyze_request = {
    'comment': { 'text': text },
    'requestedAttributes': PERSPECTIVE_ATTRS
    }

    response = client.comments().analyze(body=analyze_request).execute()
    # print(json.dumps(response, indent=2))
    
    data = response
    out = {}
    for attr, obj in data.get("attributeScores", {}).items():
        score = obj.get("summaryScore", {}).get("value")
        if score is not None:
            out[f"perspective:{attr.lower()}"] = float(score)
    return out


# 3) Google Cloud Natural Language: documents.moderateText
# REST: POST https://language.googleapis.com/v1/documents:moderateText
# https://cloud.google.com/natural-language/docs/moderating-text
# https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/moderateText
GCP_NL_URL = "https://language.googleapis.com/v1/documents:moderateText"

def classify_with_google_nl(text: str) -> Dict[str, float]:
    """
    Returns {category: probability} using Google Cloud Natural Language moderateText.
    Quick demo auth: set GOOGLE_CLOUD_API_KEY and use ?key=...
    For production, prefer OAuth service-account Bearer tokens.
    """
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_CLOUD_API_KEY")

    payload = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": text
        }
    }
    r = requests.post(
        f"{GCP_NL_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()

    # Response has moderationCategories: [{name: "...", confidence: 0..1}, ...]
    out = {}
    for cat in data.get("moderationCategories", []):
        name = cat.get("name")
        conf = cat.get("confidence")
        if name is not None and conf is not None:
            out[f"google_nl:{name}"] = float(conf)
    return out

