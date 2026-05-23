import time
import random
from scrapers.base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):

    def scrape(self, company_config: dict) -> list[dict]:
        import jobspy

        search_term = company_config.get(
            "linkedin_search",
            f"{company_config['name']} software engineer",
        )
        try:
            jobs_df = jobspy.scrape_jobs(
                site_name=["linkedin"],
                search_term=search_term,
                location="India",
                results_wanted=10,
                hours_old=24,
                country_indeed="India",
            )
            jobs = []
            for _, row in jobs_df.iterrows():
                # Prefer direct company apply URL over LinkedIn-hosted URL
                url = str(row.get("job_url_direct", "") or row.get("job_url", "") or "")
                jobs.append({
                    "title":    str(row.get("title", "") or ""),
                    "location": str(row.get("location", "") or ""),
                    "url":      url,
                })
            time.sleep(random.uniform(3, 6))
            return jobs
        except Exception as e:
            print(f"[LinkedIn] Failed for {company_config['name']}: {e}")
            return []
