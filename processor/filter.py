import re
from config import INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS
from database import db

# Catch experience-range patterns in job titles like "3+ years", "4-6 yrs", "3 to 5 years".
# Only excludes when the minimum years is >= 3 (entry-level is 0-2 years).
_EXP_RE = re.compile(
    r'\b(\d{1,2})\s*(?:\+|[-–]\s*\d{1,2})?\s*(?:to\s+\d{1,2}\s+)?(?:years?|yrs?)\b',
    re.IGNORECASE,
)
# Catch parenthesized year ranges common in Indian LinkedIn titles: "(5-7)", "(3-6)"
_PAREN_RANGE_RE = re.compile(r'\((\d{1,2})\s*[-–]\s*\d{1,2}\s*\)')


def _is_senior_by_experience(title: str) -> bool:
    m = _EXP_RE.search(title)
    if m and int(m.group(1)) >= 3:
        return True
    m2 = _PAREN_RANGE_RE.search(title)
    return bool(m2) and int(m2.group(1)) >= 3


def passes_keyword_filter(title: str) -> bool:
    t = title.lower()
    has_include = any(kw in t for kw in INCLUDE_KEYWORDS)
    has_exclude = any(kw in t for kw in EXCLUDE_KEYWORDS)
    if not has_include or has_exclude:
        return False
    return not _is_senior_by_experience(title)


def process(raw_jobs: list[dict]) -> list[dict]:
    # Step 1 — keyword filter
    filtered = [j for j in raw_jobs if passes_keyword_filter(j["title"])]

    # Step 2 — de-dupe within this run: by job_id, url, AND (company+title) to
    # collapse LinkedIn spam where the same role is posted multiple times
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    seen_company_titles: set[tuple] = set()
    deduped: list[dict] = []
    for job in filtered:
        url = job.get("url", "").strip()
        company_title_key = (job["company"].lower(), job["title"].lower().strip())
        if (job["job_id"] in seen_ids
                or (url and url in seen_urls)
                or company_title_key in seen_company_titles):
            continue
        seen_ids.add(job["job_id"])
        if url:
            seen_urls.add(url)
        seen_company_titles.add(company_title_key)
        deduped.append(job)

    # Step 3 — new-only filter (against DB — checks both job_id and url)
    new_jobs: list[dict] = []
    for job in deduped:
        if db.is_new_job(job["job_id"], job.get("url", "")):
            new_jobs.append(job)
            db.save_job(job)
        else:
            db.mark_seen(job["job_id"])

    return new_jobs
