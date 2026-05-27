"""
WhatsApp notifier via Twilio API.

Required environment variables:
  TWILIO_ACCOUNT_SID   — from console.twilio.com
  TWILIO_AUTH_TOKEN    — from console.twilio.com
  TWILIO_WHATSAPP_FROM — sender number, e.g. whatsapp:+14155238886
  WHATSAPP_TO          — your number,   e.g. whatsapp:+919876543210

Sandbox setup (free, no approval needed):
  1. Go to console.twilio.com → Messaging → Try it out → Send a WhatsApp message
  2. Follow the sandbox join instructions once from your phone
  3. Use the sandbox number as TWILIO_WHATSAPP_FROM
"""

import os
from datetime import datetime
from config import (
    INDIAN_IT_COMPANIES,
    GLOBAL_TECH_COMPANIES,
    HFT_QUANT_COMPANIES,
    INDIAN_UNICORN_COMPANIES,
    MNC_SERVICES_COMPANIES,
    FINANCE_TECH_COMPANIES,
)

# Twilio counts emojis as 2+ chars, so stay well under the 1600 limit
_CHUNK_SIZE = 1000


def _send_chunks(client, from_: str, to: str, text: str):
    import time
    lines = text.split("\n")
    chunk = ""
    for line in lines:
        addition = (line + "\n")
        if len(chunk) + len(addition) > _CHUNK_SIZE and chunk:
            msg = client.messages.create(from_=from_, to=to, body=chunk.rstrip())
            print(f"  [WhatsApp] chunk sent — sid={msg.sid} status={msg.status}")
            time.sleep(1)
            chunk = ""
        chunk += addition
    if chunk.strip():
        msg = client.messages.create(from_=from_, to=to, body=chunk.rstrip())
        print(f"  [WhatsApp] chunk sent — sid={msg.sid} status={msg.status}")
        time.sleep(1)


def send_digest(new_jobs: list[dict], health_summary: dict):
    from twilio.rest import Client

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token  = os.environ["TWILIO_AUTH_TOKEN"]
    from_number = os.environ["TWILIO_WHATSAPP_FROM"]
    to_number   = os.environ["WHATSAPP_TO"]

    client = Client(account_sid, auth_token)

    now        = datetime.now()
    time_label = "Morning" if now.hour < 12 else "Evening"
    date_str   = now.strftime("%d %b %Y")
    next_label = "6 PM" if time_label == "Morning" else "9 AM tomorrow"

    if not new_jobs:
        message = (
            f"📋 *{time_label} Digest — {date_str}*\n\n"
            f"✅ All clear — no new openings found this run\n\n"
            f"_Next update at {next_label} IST_"
        )
        _send_chunks(client, from_number, to_number, message)
        return

    # Group jobs by company
    by_company: dict[str, list[dict]] = {}
    for job in new_jobs:
        by_company.setdefault(job["company"], []).append(job)

    lines = [f"📋 *Job Digest — {time_label}, {date_str}*\n"]

    _SECTIONS = [
        ("🇮🇳 Indian IT",        INDIAN_IT_COMPANIES),
        ("🌍 Global Tech",        GLOBAL_TECH_COMPANIES),
        ("⚡ HFT / Quant",        HFT_QUANT_COMPANIES),
        ("🦄 Indian Unicorns",    INDIAN_UNICORN_COMPANIES),
        ("🏢 MNC Services",       MNC_SERVICES_COMPANIES),
        ("🏦 Finance Tech",       FINANCE_TECH_COMPANIES),
    ]

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

    # Scraper warning — only show count, not the full list
    broken = [c for c, s in health_summary.items() if s == "error"]
    if broken:
        lines.append(f"⚠️ {len(broken)} scraper(s) errored — check logs\n")

    lines.append(f"_Next update at {next_label} IST_")

    message = "\n".join(lines)
    _send_chunks(client, from_number, to_number, message)
