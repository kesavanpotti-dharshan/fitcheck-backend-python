from dotenv import load_dotenv

load_dotenv()

import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

PROMPT_TEMPLATE = """You are a resume-JD gap analyzer. Given a job description and relevant resume excerpts, identify specific gaps and matches.

Job Description:
{jd}

Relevant Resume Excerpts:
{excerpts}

Return ONLY a JSON array (no markdown, no preamble) of objects with these exact fields:
- requirement: a specific skill/requirement from the JD
- match_status: one of "match", "partial", "missing"
- evidence: quote or paraphrase from the resume excerpts supporting this, or null
- suggestion: a specific suggestion to close the gap, or null if it's a full match
"""


def analyze_gaps(jd_text: str, excerpts: list[dict]) -> tuple[list[dict], dict]:
    excerpts_text = "\n\n".join(f"[{e['section']}]\n{e['text']}" for e in excerpts)
    prompt = PROMPT_TEMPLATE.format(jd=jd_text, excerpts=excerpts_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=4000),
    )

    usage = {
        "prompt_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
        "total_tokens": response.usage_metadata.total_token_count,
    }

    raw = (response.text or "").strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].replace("json", "", 1).strip()

    if not raw:
        raise ValueError(
            "Empty response from Gemini — likely hit max_output_tokens before completing JSON."
        )

    return json.loads(raw), usage
