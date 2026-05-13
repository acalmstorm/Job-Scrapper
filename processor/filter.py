from config import INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS
from database import db


def passes_keyword_filter(title: str) -> bool:
    t = title.lower()
    has_include = any(kw in t for kw in INCLUDE_KEYWORDS)
    has_exclude = any(kw in t for kw in EXCLUDE_KEYWORDS)
    return has_include and not has_exclude


def process(raw_jobs: list[dict]) -> list[dict]:
    # Step 1 — keyword filter
    filtered = [j for j in raw_jobs if passes_keyword_filter(j["title"])]

    # Step 2 — de-dupe within this run (same job from careers + LinkedIn)
    seen_ids: set[str] = set()
    deduped: list[dict] = []
    for job in filtered:
        if job["job_id"] not in seen_ids:
            seen_ids.add(job["job_id"])
            deduped.append(job)

    # Step 3 — new-only filter (against DB)
    new_jobs: list[dict] = []
    for job in deduped:
        if db.is_new_job(job["job_id"]):
            new_jobs.append(job)
            db.save_job(job)
        else:
            db.mark_seen(job["job_id"])

    return new_jobs
