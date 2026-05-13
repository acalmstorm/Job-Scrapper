import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from config import COMPANY_CONFIGS

_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def _nested_get(obj: dict, dotted_key: str):
    """Traverse nested dict with dot-separated key path, e.g. 'a.b.c'."""
    for key in dotted_key.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


class APICareersScraper(BaseScraper):

    def scrape(self, company_config: dict) -> list[dict]:
        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        results = []
        page = 1
        while page <= 5:
            url = cfg["api_url"].replace("__PAGE__", str(page))
            try:
                resp = requests.get(url, timeout=15, headers=_HEADERS)
                resp.raise_for_status()
                data = resp.json()
            except Exception:
                break

            jobs_key   = cfg.get("jobs_key", "jobs")
            jobs_list  = _nested_get(data, jobs_key) or []

            if not jobs_list:
                break

            for job in jobs_list:
                title    = job.get(cfg.get("title_field", "title"), "")
                location = job.get(cfg.get("location_field", "location"), "")
                # location may be a list (Google)
                if isinstance(location, list):
                    location = ", ".join(str(l) for l in location)

                raw_id  = job.get(cfg.get("job_id_field", "id"), "")
                url_field = cfg.get("apply_url_field", cfg.get("job_id_field", "id"))
                path    = job.get(url_field, "")
                prefix  = cfg.get("apply_url_prefix", "")
                apply_url = f"{prefix}{path}" if path else ""

                results.append({"title": str(title), "location": str(location), "url": apply_url})

            page += 1

        return results


class PlaywrightCareersScraper(BaseScraper):

    def scrape(self, company_config: dict) -> list[dict]:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page    = browser.new_page(extra_http_headers=_HEADERS)
            try:
                page.goto(cfg["careers_url"], timeout=30_000)
                page.wait_for_selector(cfg["job_card_selector"], timeout=10_000)
                cards = page.query_selector_all(cfg["job_card_selector"])
                for card in cards:
                    title_el    = card.query_selector(cfg["title_selector"])
                    location_el = card.query_selector(cfg["location_selector"])
                    link_el     = card.query_selector(cfg["link_selector"])

                    title    = title_el.inner_text().strip()    if title_el    else ""
                    location = location_el.inner_text().strip() if location_el else ""
                    href     = link_el.get_attribute("href")    if link_el     else ""
                    # Make relative URLs absolute
                    if href and href.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(cfg["careers_url"])
                        href   = f"{parsed.scheme}://{parsed.netloc}{href}"

                    jobs.append({"title": title, "location": location, "url": href or ""})
            except PWTimeout:
                pass
            finally:
                browser.close()

        return jobs


class RequestsCareersScraper(BaseScraper):

    def scrape(self, company_config: dict) -> list[dict]:
        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        try:
            if cfg.get("method", "GET").upper() == "POST":
                resp = requests.post(
                    cfg["careers_url"], json=cfg.get("payload", {}),
                    timeout=15, headers=_HEADERS
                )
            else:
                resp = requests.get(cfg["careers_url"], timeout=15, headers=_HEADERS)
            resp.raise_for_status()
        except Exception:
            return []

        soup  = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(cfg.get("job_card_selector", "div.job"))
        jobs  = []
        for card in cards:
            title_el    = card.select_one(cfg.get("title_selector",    "h3"))
            location_el = card.select_one(cfg.get("location_selector", "span.location"))
            link_el     = card.select_one(cfg.get("link_selector",     "a"))

            href = link_el.get("href", "") if link_el else ""
            if href and href.startswith("/"):
                from urllib.parse import urlparse
                parsed = urlparse(cfg["careers_url"])
                href   = f"{parsed.scheme}://{parsed.netloc}{href}"

            jobs.append({
                "title":    title_el.get_text(strip=True)    if title_el    else "",
                "location": location_el.get_text(strip=True) if location_el else "",
                "url":      href,
            })

        return jobs


def get_scraper(scraper_type: str) -> BaseScraper:
    if scraper_type == "api":
        return APICareersScraper()
    elif scraper_type == "playwright":
        return PlaywrightCareersScraper()
    else:
        return RequestsCareersScraper()
