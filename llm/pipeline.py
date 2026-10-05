"""
Orchestrates the LLM enrichment stage: for each new job, fetch its description text
and call enrich_job(), running jobs concurrently the same way main.py's scrapers do.

This stage only adds fields — it never filters jobs out. A job that fails to enrich
(no API key set, a transient API error, an unparsable response) still ships in the
digest with its enrichment fields left as None/[] rather than being dropped.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from llm.enrich import enrich_job
from llm.profile import USER_PROFILE
from scrapers.description_fetcher import fetch_description

# Real money per call — cap how many *new* jobs get enriched in a single run.
# New-job counts per run are typically small (new postings since the last run,
# already past the keyword filter), so this is a safety net, not a normal limit.
MAX_JOBS_TO_ENRICH = 40
_WORKERS = 6

_ENRICH_DEFAULTS = {"skills": [], "stack": [], "seniority": None, "match_score": None, "pitch": None}


def _enrich_one(job: dict) -> dict:
    description = fetch_description(job.get("url", ""))
    result = enrich_job(job, description, USER_PROFILE)
    return {**job, **(result or _ENRICH_DEFAULTS)}


def enrich_jobs(jobs: list[dict]) -> list[dict]:
    """
    Enriches up to MAX_JOBS_TO_ENRICH jobs with LLM-extracted skills/stack/seniority,
    a profile match_score, and a one-line tailored pitch. Returns all jobs (enriched
    ones plus any over the cap, unenriched), sorted with the highest match_score first
    so the digest leads with the most relevant postings.
    """
    if not jobs:
        return jobs

    to_enrich, overflow = jobs[:MAX_JOBS_TO_ENRICH], jobs[MAX_JOBS_TO_ENRICH:]
    if overflow:
        print(f"  [LLM] {len(overflow)} new job(s) beyond the {MAX_JOBS_TO_ENRICH}-per-run cap — sent unenriched")

    enriched: list[dict] = []
    with ThreadPoolExecutor(max_workers=_WORKERS) as executor:
        futures = {executor.submit(_enrich_one, job): job for job in to_enrich}
        for future in as_completed(futures):
            enriched.append(future.result())

    results = enriched + [{**job, **_ENRICH_DEFAULTS} for job in overflow]
    # Jobs with a score sort first (highest first); unscored jobs keep their place at the end.
    results.sort(key=lambda j: (j.get("match_score") is None, -(j.get("match_score") or 0)))
    return results
