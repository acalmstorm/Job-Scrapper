"""
LLM enrichment — reads a scraped job (title + company + best-effort description text)
and extracts structured hiring signal via a forced tool call to Claude Haiku.

Required environment variable:
  ANTHROPIC_API_KEY  — from https://console.anthropic.com/settings/keys
  Add it to your local .env for manual runs, and as a GitHub Actions secret
  (Settings → Secrets and variables → Actions) for the scheduled workflow.

Why a forced tool call instead of asking for JSON in prose: tool_choice pins the
model to this exact schema, so block.input below is already a parsed, type-checked
dict — no prompt-engineered "respond only with JSON" and no manual json.loads() that
can fail on a stray code fence or trailing sentence.
"""

import os
import json

try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover - surfaced clearly at call time instead
    Anthropic = None

_MODEL = "claude-haiku-4-5-20251001"

_EXTRACT_TOOL = {
    "name": "extract_job_match",
    "description": (
        "Extract structured hiring signal from a job posting and score it against "
        "the candidate profile provided in the prompt."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Concrete skills explicitly required or strongly implied by the "
                    "posting (e.g. 'Python', 'distributed systems', 'SQL'). Max 10."
                ),
            },
            "stack": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "The core technology stack named in the posting — languages, "
                    "frameworks, cloud/infra. Max 8. Empty list if none is named."
                ),
            },
            "seniority": {
                "type": "string",
                "enum": ["entry", "junior", "mid", "senior", "unclear"],
                "description": (
                    "Seniority level implied by the title and description together, "
                    "not the title alone — a title can under- or over-state it."
                ),
            },
            "match_score": {
                "type": "integer",
                "description": (
                    "0-100: how well this role matches the candidate profile. "
                    "100 = ideal fit. Be honest and use the full range — most roles "
                    "should NOT score above 85."
                ),
            },
            "pitch": {
                "type": "string",
                "description": (
                    "One tailored sentence, under 220 characters, the candidate could "
                    "open an application with — it must name a specific, real "
                    "connection between their background and this exact role. No "
                    "generic filler like 'I am a great fit for this position.'"
                ),
            },
        },
        "required": ["skills", "stack", "seniority", "match_score", "pitch"],
        "additionalProperties": False,
    },
    "strict": True,
}

_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or Anthropic is None:
        return None
    _client = Anthropic(api_key=api_key)
    return _client


def _build_prompt(job: dict, description: str, profile: dict) -> str:
    desc_block = description or (
        "(Description text unavailable — this posting renders client-side and "
        "couldn't be fetched as plain HTML. Infer cautiously from the title and "
        "company alone, and reflect that uncertainty with a lower match_score if "
        "the title is ambiguous about seniority or stack.)"
    )
    return f"""Candidate profile:
{json.dumps(profile, indent=2)}

Job posting:
Company: {job.get('company', '')}
Title: {job.get('title', '')}
Location: {job.get('location', '')}

Description:
{desc_block}

Extract the structured fields and score this posting against the candidate profile."""


def enrich_job(job: dict, description: str, profile: dict) -> dict | None:
    """
    Returns {skills, stack, seniority, match_score, pitch} or None.

    Never raises — a missing API key, a rate limit, or a malformed response all
    degrade to None so the caller can ship the job un-enriched rather than drop it
    or crash the run. See llm/pipeline.py for how callers are expected to merge this.
    """
    client = _get_client()
    if client is None:
        return None

    try:
        resp = client.messages.create(
            model=_MODEL,
            max_tokens=1024,
            temperature=0,
            tools=[_EXTRACT_TOOL],
            tool_choice={"type": "tool", "name": "extract_job_match"},
            messages=[{"role": "user", "content": _build_prompt(job, description, profile)}],
        )
    except Exception as e:
        print(f"    [LLM] {job.get('company')} / {job.get('title')}: call failed — {e}")
        return None

    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" and block.name == "extract_job_match":
            result = dict(block.input)
            # The schema asks for an int 0-100; clamp defensively against drift.
            try:
                result["match_score"] = max(0, min(100, int(result.get("match_score", 0))))
            except (TypeError, ValueError):
                result["match_score"] = 0
            return result

    print(f"    [LLM] {job.get('company')} / {job.get('title')}: no tool_use block in response")
    return None
