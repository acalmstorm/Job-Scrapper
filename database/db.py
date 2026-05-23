import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

# this is a comment 

DB_PATH = Path(__file__).parent.parent / "data" / "jobs.db"

_run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
_new_job_ids_this_run: set[str] = set()


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init():
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS seen_jobs (
                job_id     TEXT PRIMARY KEY,
                company    TEXT NOT NULL,
                title      TEXT NOT NULL,
                location   TEXT,
                url        TEXT,
                source     TEXT,
                first_seen DATETIME NOT NULL,
                last_seen  DATETIME NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_seen_jobs_url ON seen_jobs (url);

            CREATE TABLE IF NOT EXISTS scraper_health (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                company   TEXT NOT NULL,
                run_at    DATETIME NOT NULL,
                jobs_found INTEGER NOT NULL DEFAULT 0,
                status    TEXT NOT NULL,
                error_msg TEXT
            );
        """)


def is_new_job(job_id: str, url: str = "") -> bool:
    try:
        with _conn() as con:
            row = con.execute(
                "SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            if row:
                return False
            if url:
                row = con.execute(
                    "SELECT 1 FROM seen_jobs WHERE url = ?", (url,)
                ).fetchone()
        return row is None
    except sqlite3.OperationalError:
        # Tables don't exist yet — auto-init and treat as new
        init()
        return True


def save_job(job: dict):
    now = datetime.now().isoformat()
    with _conn() as con:
        con.execute(
            """
            INSERT OR IGNORE INTO seen_jobs
                (job_id, company, title, location, url, source, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job["job_id"],
                job["company"],
                job["title"],
                job.get("location", ""),
                job.get("url", ""),
                job.get("source", ""),
                now,
                now,
            ),
        )
    _new_job_ids_this_run.add(job["job_id"])


def mark_seen(job_id: str):
    now = datetime.now().isoformat()
    with _conn() as con:
        con.execute(
            "UPDATE seen_jobs SET last_seen = ? WHERE job_id = ?",
            (now, job_id),
        )


def get_new_jobs_this_run(run_id: str | None = None) -> list[dict]:
    if not _new_job_ids_this_run:
        return []
    placeholders = ",".join("?" * len(_new_job_ids_this_run))
    with _conn() as con:
        rows = con.execute(
            f"SELECT job_id, company, title, location, url, source FROM seen_jobs WHERE job_id IN ({placeholders})",
            tuple(_new_job_ids_this_run),
        ).fetchall()
    return [
        {"job_id": r[0], "company": r[1], "title": r[2],
         "location": r[3], "url": r[4], "source": r[5]}
        for r in rows
    ]


def log_health(company: str, count: int, status: str, error: str | None = None):
    now = datetime.now().isoformat()
    with _conn() as con:
        con.execute(
            """
            INSERT INTO scraper_health (company, run_at, jobs_found, status, error_msg)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company, now, count, status, error),
        )


def get_health_summary() -> dict[str, str]:
    """Returns {company: status} for the most recent entry per company."""
    with _conn() as con:
        rows = con.execute(
            """
            SELECT company, status
            FROM scraper_health
            WHERE run_at = (
                SELECT MAX(run_at) FROM scraper_health AS h2
                WHERE h2.company = scraper_health.company
            )
            """
        ).fetchall()
    return {row[0]: row[1] for row in rows}
