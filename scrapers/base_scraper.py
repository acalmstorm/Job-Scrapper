from abc import ABC, abstractmethod
import hashlib
import re


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self, company_config: dict) -> list[dict]:
        """Scrape jobs for one company. Returns list of raw job dicts."""
        raise NotImplementedError

    def normalize(self, raw: dict, company_name: str, source: str) -> dict:
        """
        Normalizes any raw job dict into the standard schema:
        { job_id, company, title, location, url, source }
        """
        title    = raw.get("title", "").strip()
        location = raw.get("location", "").strip()
        url      = raw.get("url", "").strip()

        native_id = self._extract_id_from_url(url)
        job_id = native_id if native_id else self._hash_id(company_name, title, location)

        return {
            "job_id":   job_id,
            "company":  company_name,
            "title":    title,
            "location": location,
            "url":      url,
            "source":   source,
        }

    def _hash_id(self, company: str, title: str, location: str) -> str:
        raw = f"{company}|{title}|{location}".lower()
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _extract_id_from_url(self, url: str) -> str | None:
        match = re.search(r'/(\d{5,})', url)
        return match.group(1) if match else None
