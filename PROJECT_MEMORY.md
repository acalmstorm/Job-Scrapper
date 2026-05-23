# IT Job Tracker — Project Memory

> **Purpose**: Paste this file at the start of any new Claude session to restore full context.
> **Last updated**: 2026-05-23 (Session 3 complete)

---

## What This Project Does

Automated IT job scraper that runs twice daily (9 AM + 6 PM IST), scrapes ~150+ companies' career pages, filters for **early-career** software engineering roles in India, and sends a formatted WhatsApp digest via Twilio.

---

## Project Structure

```
it-job-tracker/
├── main.py                      # Entry point — orchestrates scraping + notification
├── config.py                    # COMPANY_CONFIGS, INCLUDE/EXCLUDE keywords, company lists
├── scrapers/
│   ├── base_scraper.py          # BaseScraper ABC + normalize() + job_id hashing
│   ├── careers_scraper.py       # 5 scraper classes (API, Playwright, Requests, Greenhouse, Lever, Workday)
│   ├── linkedin_scraper.py      # jobspy-based LinkedIn fallback scraper
│   └── company_configs.py       # (legacy, config now in config.py)
├── processor/
│   └── filter.py                # Keyword filter + experience-year regex + DB dedup
├── notifier/
│   └── whatsapp_bot.py          # Twilio WhatsApp digest sender (chunked, grouped by section)
├── database/
│   └── db.py                    # SQLite — job dedup, health logging
└── data/
    └── jobs.db                  # SQLite DB (auto-created)
```

---

## How Scraping Works

### Career Page Scrapers (`careers_scraper.py`)
Five scraper types, selected by `company["type"]` in config:

| Type | How it works | Companies |
|------|-------------|-----------|
| `api` | Direct JSON API call (paginated) | Google, Amazon, Microsoft |
| `greenhouse` | Greenhouse ATS public API (`boards-api.greenhouse.io`) | Stripe, Datadog, GitLab, etc. |
| `lever` | Lever ATS public API (`api.lever.co/v0/postings`) | Atlassian, Dream11 |
| `workday_api` | Workday CXS internal POST API | Nvidia, Zoom, CrowdStrike, Cadence, NetApp, etc. |
| `playwright` | Headless Chromium — CSS selectors | Most Indian companies |
| `requests` | BeautifulSoup HTML parsing | Zerodha, HFT firms, etc. |

### LinkedIn Scraper (`linkedin_scraper.py`)
- Uses `jobspy` library
- **FALLBACK ONLY** — only runs when the career page scraper returns zero results
- This avoids LinkedIn URLs showing up for companies whose own portal worked
- Uses `job_url_direct` (actual company apply URL) first, falls back to `job_url` (LinkedIn URL)
- `hours_old=24`, `results_wanted=10`, `location="India"`

### Job ID Generation (`base_scraper.py`)
```python
def normalize(raw, company_name, source):
    url = raw["url"]
    native_id = re.search(r'/(\d{5,})', url)  # extract numeric ID from URL
    job_id = native_id or sha256(f"{company}|{title}|{location}")[:16]
```

---

## Filtering Logic (`processor/filter.py`)

Three-stage pipeline:

1. **Keyword filter** — title must match an INCLUDE keyword AND not match any EXCLUDE keyword, AND not contain an experience-year pattern indicating 3+ years required
2. **In-run dedup** — by `job_id` and `url` (same job from two sources is deduped)
3. **DB dedup** — only truly new jobs (not seen in any prior run) are sent

### INCLUDE_KEYWORDS (must match one)
```
software engineer, sde, developer, fullstack, full stack, backend, frontend,
front-end, back-end, software development, platform engineer, site reliability,
sre, devops, associate engineer, junior engineer, junior developer,
graduate engineer, new grad
```

### EXCLUDE_KEYWORDS (must match none)
```
manager, director, vp, intern, principal, architect, staff engineer, senior,
sr., sr , " lead", "lead ", advisor, head of, tech lead, sales, marketing,
recruiter, hr, finance,
sde 2, sde-2, sde2, sde ii,
engineer ii, engineer 2, engineer iii, engineer 3,
software engineer 2, software engineer ii, software engineer iii, software engineer 3,
level 5, level 6, " l5", " l6",
mid-level, mid level, experienced, staff, distinguished, fellow,
freelance, freelancer,
developer ii, developer 2, developer iii, developer 3, developer iv, developer 4,
sre ii, sre 2, mid-senior,
software developer 2, software developer ii, software developer iii, software developer 3, software developer 4, software developer 5,
" l4", smts, lmts, contract
```

### Experience-Year Regex (added 2026-05-23)
```python
_EXP_RE = re.compile(r'\b(\d{1,2})\s*(?:\+|[-–]\s*\d{1,2})?\s*(?:to\s+\d{1,2}\s+)?(?:years?|yrs?)\b')
# Blocks if minimum years >= 3
# Passes: "0-2 years", "1-3 years", "2+ years"
# Blocks: "3+ years", "4-6 yrs", "3 to 5 years", "8+ yrs"

_PAREN_RANGE_RE = re.compile(r'\((\d{1,2})\s*[-–]\s*\d{1,2}\s*\)')
# Catches Indian LinkedIn titles with parenthesized ranges like "(5-7)", "(3-6)"
# Blocks if minimum of range >= 3
# Blocks: "(5-7)", "(3-6)", "(4-8)"
# Passes: "(0-2)", "(1-3)"
```

---

## Company Config Structure

Each company in `COMPANY_CONFIGS` dict:
```python
"CompanyName": {
    "type": "greenhouse" | "lever" | "workday_api" | "api" | "playwright" | "requests",
    "careers_url": "...",
    "linkedin_search": "Company Software Engineer India",  # for jobspy fallback
    # type-specific fields:
    "greenhouse_board_token": "...",      # greenhouse only
    "lever_company": "...",               # lever only
    "workday_host": "...",                # workday only
    "workday_tenant": "...",
    "workday_job_board": "...",
    "api_url": "...",                     # api type only
    "job_card_selector": "...",           # playwright/requests
    "title_selector": "...",
    "location_selector": "...",
    "link_selector": "...",
    "apply_url_prefix": "...",
    "region": "global" | "indian_it" | "hft_quant" | "indian_unicorn" | "mnc_services" | "finance_tech",
    "entry_lpa": "20-35",                 # informational
}
```

---

## Companies (~150 total, grouped in config.py)

### Section 1: Global Tech Giants
Google, Microsoft, Amazon, Meta, Apple, IBM, Salesforce, Adobe, SAP, Oracle,
Flexport, Atlassian, Nvidia, Intel, Cisco, ThoughtWorks, Samsung, Qualcomm, AMD,
Texas Instruments, Uber, Netflix, PayPal, Walmart, Zoom, LinkedIn, Stripe,
Booking.com, Akamai, AppDynamics, Arista Networks, ServiceNow, Twilio, Okta,
Datadog, Confluent, HashiCorp, GitLab

### Section 2: HFT / Quant
Tower Research Capital, Graviton Research Capital, QuadEye Securities,
Quantbox Research, Optiver, IMC Trading, WorldQuant, AlphaGrep,
Jane Street, Two Sigma, Squarepoint Capital

### Section 3: Indian IT Services
TCS, Infosys, Wipro, HCL Tech, Tech Mahindra, Cognizant, Hexaware, Mphasis,
LTIMindtree, Persistent Systems, Coforge, Birlasoft, Zensar, Happiest Minds, Nagarro

### Section 4: MNC Services & Consulting
Accenture, Deloitte, Capgemini, Publicis Sapient, Genpact, EXL Analytics

### Section 5: Indian Unicorns & Startups
Flipkart, Zomato, Swiggy, PhonePe, Razorpay, Meesho, Zerodha, CRED, Groww,
Nykaa, Freshworks, ShareChat, OYO, Delhivery, Ola, Jio, Paytm, Urban Company,
Unacademy, InMobi, MakeMyTrip, BrowserStack, Juspay, Chargebee, Druva,
Darwinbox, CleverTap, MoEngage, Innovaccer, Samsara,
Dream11, Games24x7, WinZO, Upstox, Angel One, INDMoney, CoinDCX, Tata 1mg,
PharmEasy, ClearTax, IndiaMart, Ninjacart, Lenskart, Zepto, Yellow AI, Gupshup, Leena AI

### Section 6: Cloud / DevTools / SaaS
Databricks, Snowflake, MongoDB, Palo Alto Networks, CrowdStrike, Nutanix,
Rubrik, Sprinklr, Postman, Pure Storage, Cohesity,
Cadence, Synopsys, KLA, Ansys, MathWorks, Autodesk,
Western Digital, NetApp, Broadcom, Commvault,
Intuit, Mastercard, Rippling, Workday, Zendesk, HubSpot,
Zscaler, SentinelOne, Fortinet, Wiz, Netskope,
Juniper Networks, Eightfold AI

### Section 7: Finance / Banking Tech
Goldman Sachs, Morgan Stanley, JP Morgan, Deutsche Bank, DE Shaw, Arcesium,
Barclays, HSBC Technology, American Express, Visa, BlackRock, BNY Mellon,
Citi, Standard Chartered, Fidelity Investments

---

## Notification Format (WhatsApp via Twilio)

```
📋 *Job Digest — Morning, 23 May 2026*

*── 🌍 Global Tech ──*
  *Google* — 2 new openings
    • Software Engineer, Site Reliability — Bangalore
      Apply: https://careers.google.com/jobs/results/...
    • Associate Software Engineer — Hyderabad
      Apply: https://careers.google.com/jobs/results/...

*── 🦄 Indian Unicorns ──*
  ...

⚠️ 12 scraper(s) errored — check logs

_Next update at 6 PM IST_
```

- Messages chunked at 1000 chars (Twilio WhatsApp limit consideration)
- Jobs grouped by section (Indian IT → Global Tech → HFT → Unicorns → MNC → Finance)

---

## Environment Variables Required

```
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+91XXXXXXXXXX
```

---

## Bugs Fixed History

### Session 1 (date unknown — conversation lost)
- Fixed various scraping bugs (details lost)
- Added senior-role filtering keywords
- Set up multi-source scraping (career page + LinkedIn)

### Session 2 (2026-05-23)

**Bug 1 — LinkedIn URLs showing up instead of company URLs**
- Root cause: `linkedin_scraper.py` always used `job_url` (LinkedIn-hosted URL)
- Fix: Use `job_url_direct` first, fall back to `job_url`
- File: `scrapers/linkedin_scraper.py`

**Bug 2 — LinkedIn running alongside career scraper (causing duplicates + LinkedIn URLs)**
- Root cause: LinkedIn ran for every company regardless of whether career page worked
- Fix: LinkedIn is now a fallback — only runs when career page scraper returns zero results
- File: `main.py` → `_scrape_company()`

**Bug 3 — Senior roles slipping through ("Developer II", "4+ years" titles)**
- Root cause 1: `EXCLUDE_KEYWORDS` covered "engineer ii" but not "developer ii", "developer 2" etc.
- Root cause 2: No filter for experience-range patterns in titles (common in Indian LinkedIn postings)
- Fix 1: Added `developer ii/2/iii/3/iv/4`, `sre ii/2`, `mid-senior` to EXCLUDE_KEYWORDS
- Fix 2: Added regex `_EXP_RE` in `processor/filter.py` — blocks if min years in title ≥ 3
- Files: `config.py`, `processor/filter.py`

**Bug 4 — Parenthesized year ranges "(5-7)" in titles not caught**
- Root cause: `_EXP_RE` requires explicit "years"/"yrs" word — common Indian LinkedIn format `(5-7)` has no such word
- Fix: Added `_PAREN_RANGE_RE = re.compile(r'\((\d{1,2})\s*[-–]\s*\d{1,2}\s*\)')` in `filter.py`
- `_is_senior_by_experience()` now checks both regexes
- File: `processor/filter.py`

**Bug 5 — Repeated same job across multiple WhatsApp notifications**
- Root cause: In-run dedup was only by `job_id` and `url`, but LinkedIn sometimes returns the same role with slightly different IDs (LinkedIn spam)
- Fix: Added `(company, title_lower)` tuple as a third dedup key inside `process()` in `filter.py`
- File: `processor/filter.py`

**Bug 6 — Database was never initialized (0-byte jobs.db), every run treated all jobs as new**
- Root cause: `is_new_job()` threw `OperationalError` when tables didn't exist, which propagated as an exception and skipped saving — so no job was ever written to DB
- Fix: Wrapped `is_new_job()` in try/except `OperationalError` → auto-calls `init()` and returns `True`
- Effect: DB tables now auto-create on first use; cross-run dedup now actually works
- File: `database/db.py`

**Bug 7 — Additional senior level titles slipping through**
- Added to EXCLUDE_KEYWORDS: `software developer 2/3/4/5/ii/iii`, `" l4"`, `smts`, `lmts`, `contract`
- `smts`/`lmts` = Salesforce/Juniper level designations (Senior/Lead Member of Technical Staff)
- `" l4"` = mid-level at most FAANG companies
- File: `config.py`

**Validation**: All 29 filter test cases pass (verified 2026-05-23)

---

### Session 3 (2026-05-23 — same day, continued)

**Bug 8 — SDE 3 / SDE 4 not filtered (Dream11 "SDE 3 - DevOps")**
- Root cause: Only `sde 2` variants were in EXCLUDE_KEYWORDS, not level 3+
- Fix: Added `sde 3`, `sde-3`, `sde3`, `sde iii`, `sde 4`, `sde-4`, `sde4`, `sde iv`
- File: `config.py`

**Bug 9 — "SDET - 2" trailing level suffix not caught**
- Root cause: `(SDET) - 2` has a paren before `- 2` so substring match `sdet - 2` doesn't work
- Fix: Added `_TRAILING_LEVEL_RE = re.compile(r'[-–]\s*([2-9])\s*$')` — catches ` - N` at end of title where N ≥ 2
- File: `processor/filter.py`

**Bug 10 — "Vice President" not filtered (Citi titles)**
- Root cause: Only `vp` in EXCLUDE_KEYWORDS, not the full form
- Fix: Added `vice president`
- File: `config.py`

**Bug 11 — "Custom Software Engineer" LinkedIn placeholder spam**
- Root cause: LinkedIn uses this as a placeholder title when it can't index the actual title; appeared for 8+ companies
- Fix: Added `custom software engineer` to EXCLUDE_KEYWORDS — it's never a real job title
- File: `config.py`

**Bug 12 — Support/consulting roles passing filter**
- Root cause: `Developer Support Engineer` (Okta) and `DevOps Consultant` (MongoDB) have no exclude keyword
- Fix: Added `developer support`, `consultant`
- File: `config.py`

**Bug 13 — "Engineer lll" (lowercase L fake Roman numeral) not caught**
- Root cause: LinkedIn sometimes renders `III` with lowercase `l` characters; `engineer iii` keyword doesn't match `engineer lll`
- Fix: Added `engineer lll`, `engineer ll` to EXCLUDE_KEYWORDS
- File: `config.py`

**Bug 14 — Amazon (and others) returning non-India jobs**
- Root cause: `APICareersScraper` collected all results without location filtering; Greenhouse/Lever/Workday all filtered, but the generic API scraper didn't
- Fix: Added `_is_india_location()` check inside `APICareersScraper.scrape()` — skips jobs with a non-empty location that doesn't match India keywords
- File: `scrapers/careers_scraper.py`

**Bug 15 — WhatsApp messages stopped after 2 days (Twilio sandbox session)**
- Root cause: Twilio WhatsApp Sandbox requires the user to stay "joined" — session expires after ~24h of inactivity from the user's side. When Twilio throws, `send_digest()` crashed with no error handling, causing GitHub Actions to silently fail (red ✗). User didn't notice because they only checked WhatsApp.
- Fix: Added try/except around `send_digest()` in `main.py` with clear error print + re-raise. Added SID/status logging per chunk in `whatsapp_bot.py` so logs show delivery status.
- **User action required**: Re-join Twilio sandbox by sending the join keyword to `+14155238886` on WhatsApp whenever messages stop.
- Files: `main.py`, `notifier/whatsapp_bot.py`

**Architecture insight — Why ~90% of results are LinkedIn URLs:**
- 128/166 companies (77%) were configured as `playwright` scraper type
- Playwright scrapers fail in GitHub Actions because headless Chromium on cloud runners is trivially detected as a bot by Cloudflare/DataDome on most career sites
- When playwright scraper returns zero (or errors), LinkedIn fallback kicks in → LinkedIn URLs
- Only Greenhouse, Lever, Workday scrapers are reliable (pure public JSON APIs, no bot detection)

**Fix — Switched 13 companies from playwright to proper API scrapers:**

| Company | From | To | Token/Host |
|---------|------|----|------------|
| HubSpot | playwright | greenhouse | `hubspotjobs` |
| Zscaler | playwright | greenhouse | `zscaler` |
| SentinelOne | playwright | greenhouse | `sentinellabs` |
| Wiz | playwright | greenhouse | `wizinc` |
| Razorpay | playwright | greenhouse | `razorpaysoftwareprivatelimited` |
| Intel | playwright | workday_api | `intel.wd1.myworkdayjobs.com / External` |
| Netflix | playwright | workday_api | `netflix.wd1.myworkdayjobs.com / Netflix` |
| BrowserStack | playwright | workday_api | `browserstack.wd3.myworkdayjobs.com / External` |
| Visa | playwright | workday_api | `visa.wd5.myworkdayjobs.com / Visa` |
| BlackRock | playwright | workday_api | `blackrock.wd1.myworkdayjobs.com / BlackRock_Professional` |
| Broadcom | playwright | workday_api | `broadcom.wd1.myworkdayjobs.com / External_Career` |
| Mastercard | playwright | workday_api | `mastercard.wd1.myworkdayjobs.com / CorporateCareers` |
| Meesho | playwright | lever | `meesho` |

**Playwright remaining**: 115 companies (down from 128)

**ATS research findings for remaining playwright companies (do NOT convert — wrong ATS):**
- Freshworks → SmartRecruiters (`careers.smartrecruiters.com/Freshworks`)
- Palo Alto Networks → SmartRecruiters (`paloaltonetworks2`)
- Western Digital → SmartRecruiters
- Wipro → SAP SuccessFactors
- Chargebee → SAP SuccessFactors
- Synopsys → Avature
- HSBC Technology → Eightfold AI
- American Express → Eightfold AI
- AMD → iCIMS
- Flipkart → TurboHire (Indian ATS)
- Nutanix → Jobvite
- Rippling → Own ATS (`ats.rippling.com`)
- Fortinet → Oracle Cloud HCM
- Swiggy → Darwinbox (Indian ATS)
- Eightfold AI → Their own platform

**Permanent LinkedIn companies (use LinkedIn Easy Apply only — no external URL exists):**
TCS, Infosys, HCL Tech, Wipro, Cognizant, Tech Mahindra, Mphasis, Accenture, Capgemini — these Indian IT companies only accept applications through LinkedIn Easy Apply on their LinkedIn posts. The `linkedin.com/jobs/view/` URL IS the correct apply link for these.

---

## Known Limitations / Future Work

- **115 playwright scrapers still unreliable** — returning zero and falling back to LinkedIn
- Next improvement: build SmartRecruiters scraper (covers Freshworks, Palo Alto, Western Digital)
- Next improvement: build iCIMS XML feed scraper (covers AMD and others)
- Greenhouse, Lever, Workday API scrapers are the most reliable (pure API, no DOM)
- LinkedIn (`jobspy`) may be rate-limited by LinkedIn — if blocked, fallback results will be empty
- `hours_old=24` in LinkedIn scraper means a job must be posted in last 24h to appear
- No retry logic on failed scrapers
- **Twilio sandbox**: re-join by sending join keyword to sandbox number whenever messages stop

---

## User Profile

- **Experience level**: Early career (0–2 years) — wants entry-level / junior / associate / new-grad roles only
- **Target**: India-based roles (Bangalore, Hyderabad, Pune, Mumbai, Gurgaon, Delhi NCR, remote India)
- **Notification**: WhatsApp via Twilio sandbox
