import re
import requests
from bs4 import BeautifulSoup

_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
_MAX_CHARS = 6000


def fetch_description(url: str, max_chars: int = _MAX_CHARS) -> str:
    """
    Best-effort fetch of a job posting's visible text, for feeding to the LLM
    enrichment step. Works well for server-rendered ATS pages — Greenhouse, Lever,
    and most of the "requests"-type company pages already render full text in the
    initial HTML. Returns "" for JS-rendered SPAs (Meta, Flipkart, Zomato, etc. —
    the ones scraped via Playwright) or on any network failure; enrich_job() treats
    an empty description as "infer from title/company only" rather than failing.
    """
    if not url:
        return ""
    try:
        resp = requests.get(url, timeout=12, headers=_HEADERS)
        resp.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]
