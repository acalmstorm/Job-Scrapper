import time
import random
from datetime import datetime

from config import COMPANY_CONFIGS, ALL_COMPANIES
from scrapers.careers_scraper import get_scraper
from scrapers.linkedin_scraper import LinkedInScraper
from processor import filter as job_filter
from notifier import whatsapp_bot
from database import db


def run():
    print(f"[{datetime.now()}] Job tracker run starting...")
    db.init()

    all_raw_jobs: list[dict] = []
    linkedin_scraper = LinkedInScraper()

    for name in ALL_COMPANIES:
        company = {"name": name, **COMPANY_CONFIGS.get(name, {})}
        print(f"  Scraping {name}...")

        # ── Careers page ──────────────────────────────────────────────────────
        try:
            scraper = get_scraper(company.get("type", "playwright"))
            jobs = scraper.scrape(company)
            normalized = [scraper.normalize(j, name, "careers") for j in jobs]
            status = "ok" if normalized else "zero_results"
            db.log_health(name, len(normalized), status)
            all_raw_jobs.extend(normalized)
            print(f"    Careers: {len(normalized)} jobs")
        except Exception as e:
            db.log_health(name, 0, "error", str(e))
            print(f"    Careers ERROR: {e}")

        # ── LinkedIn ──────────────────────────────────────────────────────────
        try:
            li_jobs = linkedin_scraper.scrape(company)
            li_normalized = [linkedin_scraper.normalize(j, name, "linkedin") for j in li_jobs]
            all_raw_jobs.extend(li_normalized)
            print(f"    LinkedIn: {len(li_normalized)} jobs")
        except Exception as e:
            print(f"    LinkedIn skipped: {e}")

        time.sleep(random.uniform(2, 5))

    print(f"  Total raw jobs scraped: {len(all_raw_jobs)}")

    # Filter + de-dupe
    new_jobs = job_filter.process(all_raw_jobs)
    print(f"  New jobs after filtering: {len(new_jobs)}")

    # Send WhatsApp digest
    health = db.get_health_summary()
    whatsapp_bot.send_digest(new_jobs, health)
    print(f"[{datetime.now()}] Run complete. WhatsApp digest sent.")


if __name__ == "__main__":
    run()
