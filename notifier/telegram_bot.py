"""
Telegram notifier — replaces Twilio WhatsApp sandbox.

Required environment variables:
  TELEGRAM_BOT_TOKEN  — from @BotFather
  TELEGRAM_CHAT_ID    — your personal chat ID (see setup instructions below)

Setup (one-time, 2 minutes):
  1. Open Telegram → search @BotFather → send /newbot → follow prompts → copy token
  2. Start a chat with your new bot (send it any message)
  3. Visit https://api.telegram.org/bot<TOKEN>/getUpdates in browser
     → find "chat":{"id": <NUMBER>} → that number is your TELEGRAM_CHAT_ID
  4. Add both as GitHub secrets: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
"""

import os
import time
import requests
from datetime import datetime
from config import (
    INDIAN_IT_COMPANIES,
    GLOBAL_TECH_COMPANIES,
    HFT_QUANT_COMPANIES,
    INDIAN_UNICORN_COMPANIES,
    MNC_SERVICES_COMPANIES,
    FINANCE_TECH_COMPANIES,
)

_MAX_MSG_LEN = 4000   # Telegram limit is 4096; stay under to be safe
_API_BASE    = "https://api.telegram.org/bot{token}/sendMessage"


def _send(token: str, chat_id: str, text: str):
    url  = _API_BASE.format(token=token)
    resp = requests.post(url, json={
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "Markdown",
    }, timeout=15)
    resp.raise_for_status()
    result = resp.json()
    print(f"  [Telegram] sent — message_id={result['result']['message_id']}")
    time.sleep(0.5)   # avoid hitting 30 msg/sec bot API limit


def _send_chunks(token: str, chat_id: str, text: str):
    lines = text.split("\n")
    chunk = ""
    for line in lines:
        addition = line + "\n"
        if len(chunk) + len(addition) > _MAX_MSG_LEN and chunk:
            _send(token, chat_id, chunk.rstrip())
            chunk = ""
        chunk += addition
    if chunk.strip():
        _send(token, chat_id, chunk.rstrip())


def send_digest(new_jobs: list[dict], health_summary: dict):
    token   = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    now        = datetime.now()
    time_label = "Morning" if now.hour < 12 else "Evening"
    date_str   = now.strftime("%d %b %Y")
    next_label = "6 PM" if time_label == "Morning" else "9 AM tomorrow"

    if not new_jobs:
        _send(token, chat_id,
              f"📋 *{time_label} Digest — {date_str}*\n\n"
              f"✅ No new openings this run\n\n"
              f"_Next update at {next_label} IST_")
        return

    by_company: dict[str, list[dict]] = {}
    for job in new_jobs:
        by_company.setdefault(job["company"], []).append(job)

    _SECTIONS = [
        ("🇮🇳 Indian IT",     INDIAN_IT_COMPANIES),
        ("🌍 Global Tech",     GLOBAL_TECH_COMPANIES),
        ("⚡ HFT / Quant",     HFT_QUANT_COMPANIES),
        ("🦄 Indian Unicorns", INDIAN_UNICORN_COMPANIES),
        ("🏢 MNC Services",    MNC_SERVICES_COMPANIES),
        ("🏦 Finance Tech",    FINANCE_TECH_COMPANIES),
    ]

    lines = [f"📋 *Job Digest — {time_label}, {date_str}*\n"]

    for section_label, company_list in _SECTIONS:
        section_jobs = [(c, by_company[c]) for c in company_list if c in by_company]
        if not section_jobs:
            continue
        lines.append(f"*── {section_label} ──*")
        for company, jobs in section_jobs:
            count = len(jobs)
            lines.append(f"  *{company}* — {count} new opening{'s' if count > 1 else ''}")
            for job in jobs:
                loc = job.get("location", "") or ""
                lines.append(f"    • {job['title']}" + (f" — {loc}" if loc else ""))
                if job.get("url"):
                    lines.append(f"      Apply: {job['url']}")
        lines.append("")

    broken = [c for c, s in health_summary.items() if s == "error"]
    if broken:
        lines.append(f"⚠️ {len(broken)} scraper(s) errored\n")

    lines.append(f"_Next update at {next_label} IST_")

    _send_chunks(token, chat_id, "\n".join(lines))
