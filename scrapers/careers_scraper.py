import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from config import COMPANY_CONFIGS

_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# India location keywords for filtering
_INDIA_LOCATIONS = [
    "india",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "pune",
    "mumbai",
    "gurgaon",
    "gurugram",
    "noida",
    "chennai",
    "delhi",
    "kolkata",
    "ahmedabad",
    "remote, india",
    "india remote",
]


def _is_india_location(location: str) -> bool:
    """Return True if location string refers to an India-based position."""
    loc_lower = location.lower()
    return any(keyword in loc_lower for keyword in _INDIA_LOCATIONS)


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

                location_str = str(location)
                # Skip non-India jobs (Amazon API still returns some UK/US results
                # even with loc_query=India in the URL)
                if location_str and not _is_india_location(location_str):
                    continue

                results.append({"title": str(title), "location": location_str, "url": apply_url})

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


class GreenhouseATSScraper(BaseScraper):
    """
    Scrapes jobs from the public Greenhouse ATS API.

    API: GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs
    Returns JSON: { "jobs": [ { "id", "title", "location": {"name": "..."}, "absolute_url" }, ... ] }

    Config keys:
      greenhouse_board_token  — board slug (e.g. "purestorage")
    """

    def scrape(self, company_config: dict) -> list[dict]:
        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        board_token = cfg.get("greenhouse_board_token")
        if not board_token:
            return []

        url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
        try:
            resp = requests.get(url, timeout=15, headers=_HEADERS)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"    [Greenhouse] {company_config['name']}: request failed — {e}")
            return []

        jobs_raw = data.get("jobs", [])
        results = []
        for job in jobs_raw:
            title = job.get("title", "")
            location = (job.get("location") or {}).get("name", "")
            apply_url = job.get("absolute_url", "")
            job_id = str(job.get("id", ""))

            # Only keep India-based jobs
            if not _is_india_location(location):
                continue

            results.append({
                "title":    title,
                "location": location,
                "url":      apply_url,
                "job_id":   job_id,
            })

        return results


class LeverATSScraper(BaseScraper):
    """
    Scrapes jobs from the public Lever ATS API.

    API: GET https://api.lever.co/v0/postings/{company}?mode=json
    Returns JSON array: [ { "id", "text" (title), "categories": {"location": ...}, "hostedUrl" }, ... ]

    Config keys:
      lever_company  — company slug used in Lever (e.g. "dreamsports" for Dream11)
    """

    def scrape(self, company_config: dict) -> list[dict]:
        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        lever_company = cfg.get("lever_company")
        if not lever_company:
            return []

        url = f"https://api.lever.co/v0/postings/{lever_company}?mode=json"
        try:
            resp = requests.get(url, timeout=15, headers=_HEADERS)
            resp.raise_for_status()
            postings = resp.json()
        except Exception as e:
            print(f"    [Lever] {company_config['name']}: request failed — {e}")
            return []

        if not isinstance(postings, list):
            return []

        results = []
        for posting in postings:
            title = posting.get("text", "")
            categories = posting.get("categories") or {}
            location = categories.get("location", "") or ""
            apply_url = posting.get("hostedUrl", "")
            job_id = posting.get("id", "")

            # Only keep India-based jobs; if location is empty treat as eligible
            # (some Lever boards don't tag location per-posting)
            if location and not _is_india_location(location):
                continue

            results.append({
                "title":    title,
                "location": location,
                "url":      apply_url,
                "job_id":   job_id,
            })

        return results


class WorkdayATSScraper(BaseScraper):
    """
    Scrapes jobs from Workday's internal CXS (Candidate Experience) API.

    API: POST https://{subdomain}.wd5.myworkdayjobs.com/wday/cxs/{tenant}/{job_board}/jobs
    Body: { "limit": 20, "offset": 0, "searchText": "", "locations": [{"id": "<india-id>"}] }

    The India country location ID in Workday is: bc33aa3152ec42d4995f4791a106ed09

    Config keys:
      workday_subdomain  — e.g. "nvidia"
      workday_tenant     — e.g. "NVIDIAExternalCareerSite"
      workday_job_board  — defaults to "External_Careers" if not set
      workday_host       — full host override e.g. "nvidia.wd5.myworkdayjobs.com"
                           (use when subdomain != tenant in domain)

    The careers_url in config already contains the Workday URL; we parse it to extract
    the subdomain and tenant when explicit config keys are absent.
    """

    INDIA_LOCATION_ID = "bc33aa3152ec42d4995f4791a106ed09"

    def _parse_workday_url(self, careers_url: str) -> tuple[str, str, str]:
        """
        Parse a Workday careers URL to extract (host, tenant, job_board).
        URL form: https://{host}/{tenant}?...
        e.g. https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?...
        """
        from urllib.parse import urlparse
        parsed = urlparse(careers_url)
        host = parsed.netloc  # e.g. nvidia.wd5.myworkdayjobs.com
        path_parts = [p for p in parsed.path.strip("/").split("/") if p]
        tenant = path_parts[0] if path_parts else "External_Careers"
        job_board = path_parts[1] if len(path_parts) > 1 else "External_Careers"
        return host, tenant, job_board

    def scrape(self, company_config: dict) -> list[dict]:
        cfg = COMPANY_CONFIGS.get(company_config["name"], {})
        if not cfg:
            return []

        careers_url = cfg.get("careers_url", "")

        # Allow explicit config overrides, otherwise parse from careers_url
        host = cfg.get("workday_host")
        tenant = cfg.get("workday_tenant")
        job_board = cfg.get("workday_job_board", "External_Careers")

        if not host or not tenant:
            parsed_host, parsed_tenant, parsed_board = self._parse_workday_url(careers_url)
            host = host or parsed_host
            tenant = tenant or parsed_tenant
            if not cfg.get("workday_job_board"):
                job_board = parsed_board

        api_url = f"https://{host}/wday/cxs/{tenant}/{job_board}/jobs"
        payload = {
            "limit": 20,
            "offset": 0,
            "searchText": "",
            "locations": [{"id": self.INDIA_LOCATION_ID}],
        }

        results = []
        offset = 0
        max_pages = 5

        for _ in range(max_pages):
            payload["offset"] = offset
            try:
                resp = requests.post(
                    api_url,
                    json=payload,
                    timeout=15,
                    headers={**_HEADERS, "Content-Type": "application/json"},
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"    [Workday] {company_config['name']}: request failed — {e}")
                break

            job_postings = data.get("jobPostings", [])
            if not job_postings:
                break

            base_url = f"https://{host}/{tenant}"
            for job in job_postings:
                title = job.get("title", "")
                location = job.get("locationsText", "") or job.get("primaryLocation", "") or ""
                external_path = job.get("externalPath", "")
                apply_url = f"{base_url}{external_path}" if external_path else ""
                job_id = job.get("bulletFields", [""])[0] if job.get("bulletFields") else ""
                # Fallback: extract from path
                if not job_id and external_path:
                    import re
                    m = re.search(r'/(\d{5,})', external_path)
                    job_id = m.group(1) if m else ""

                results.append({
                    "title":    title,
                    "location": location,
                    "url":      apply_url,
                    "job_id":   job_id,
                })

            total = data.get("total", 0)
            offset += len(job_postings)
            if offset >= total or offset >= 100:
                break

        return results


def get_scraper(scraper_type: str) -> BaseScraper:
    if scraper_type == "api":
        return APICareersScraper()
    elif scraper_type == "playwright":
        return PlaywrightCareersScraper()
    elif scraper_type == "greenhouse":
        return GreenhouseATSScraper()
    elif scraper_type == "lever":
        return LeverATSScraper()
    elif scraper_type == "workday_api":
        return WorkdayATSScraper()
    else:
        return RequestsCareersScraper()
