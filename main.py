import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from config import COMPANY_CONFIGS, ALL_COMPANIES
from scrapers.careers_scraper import get_scraper
from scrapers.linkedin_scraper import LinkedInScraper
from processor import filter as job_filter
from notifier import whatsapp_bot
from database import db

_thread_local = threading.local()


def _get_linkedin_scraper() -> LinkedInScraper:
    if not hasattr(_thread_local, "linkedin"):
        _thread_local.linkedin = LinkedInScraper()
    return _thread_local.linkedin


def _scrape_company(name: str) -> tuple[list[dict], list[tuple]]:
    company = {"name": name, **COMPANY_CONFIGS.get(name, {})}
    jobs: list[dict] = []
    health: list[tuple] = []

    try:
        scraper = get_scraper(company.get("type", "playwright"))
        raw = scraper.scrape(company)
        normalized = [scraper.normalize(j, name, "careers") for j in raw]
        status = "ok" if normalized else "zero_results"
        health.append((name, len(normalized), status, None))
        jobs.extend(normalized)
        print(f"  {name}: careers={len(normalized)}")
    except Exception as e:
        health.append((name, 0, "error", str(e)))
        print(f"  {name}: careers ERROR — {e}")

    try:
        li_scraper = _get_linkedin_scraper()
        li_raw = li_scraper.scrape(company)
        li_norm = [li_scraper.normalize(j, name, "linkedin") for j in li_raw]
        jobs.extend(li_norm)
        if li_norm:
            print(f"  {name}: linkedin={len(li_norm)}")
    except Exception as e:
        print(f"  {name}: linkedin skipped — {e}")

    return jobs, health


def run():
    print(f"[{datetime.now()}] Job tracker starting — {len(ALL_COMPANIES)} companies")
    db.init()

    all_raw_jobs: list[dict] = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(_scrape_company, name): name for name in ALL_COMPANIES}
        for future in as_completed(futures):
            try:
                jobs, health = future.result()
                all_raw_jobs.extend(jobs)
                for h in health:
                    db.log_health(*h)
            except Exception as e:
                print(f"  Worker error: {e}")

    print(f"  Total raw jobs scraped: {len(all_raw_jobs)}")

    new_jobs = job_filter.process(all_raw_jobs)
    print(f"  New jobs after filtering: {len(new_jobs)}")

    health_summary = db.get_health_summary()
    whatsapp_bot.send_digest(new_jobs, health_summary)
    print(f"[{datetime.now()}] Run complete. WhatsApp digest sent.")


if __name__ == "__main__":
    run()
