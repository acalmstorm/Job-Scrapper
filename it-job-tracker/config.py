import os
from dotenv import load_dotenv

load_dotenv()

MORNING_LABEL = "9 AM"
EVENING_LABEL = "6 PM"

INCLUDE_KEYWORDS = [
    "software engineer",
    "sde",
    "developer",
    "fullstack",
    "full stack",
    "backend",
    "frontend",
    "front-end",
    "back-end",
    "software development",
    "platform engineer",
    "site reliability",
    "sre",
    "devops",
]

EXCLUDE_KEYWORDS = [
    "manager",
    "director",
    "vp",
    "intern",
    "principal architect",
    "sales",
    "marketing",
    "recruiter",
    "hr",
    "finance",
]

# =============================================================================
#  COMPANY_CONFIGS — Complete IT Job Tracker Configuration
#  Total: 115 companies
#  Sections:
#    1. Global Tech Giants
#    2. HFT / Quant Firms  (NEW — all pay 40–200+ LPA at entry)
#    3. Indian IT Services
#    4. MNC IT Services & Consulting
#    5. Indian Unicorns & High-Growth Startups
#    6. Cloud / DevTools / SaaS
#    7. Finance / Banking Tech  (NEW — all pay 20+ LPA at entry)
#    8. High-Growth SaaS missing from original  (NEW — all pay 20+ LPA at entry)
#  Scraper types: "api" | "playwright" | "requests"
# =============================================================================

COMPANY_CONFIGS = {

    # =========================================================================
    # SECTION 1: GLOBAL TECH GIANTS
    # =========================================================================

    "Google": {
        "type": "api",
        "careers_url": "https://careers.google.com/jobs/results/?category=SOFTWARE_ENGINEERING&location=India",
        "api_url": "https://careers.google.com/api/jobs/results/?category=SOFTWARE_ENGINEERING&location=India&page_size=20",
        "linkedin_search": "Google Software Engineer India",
        "job_id_field": "job_id",
        "title_field": "title",
        "location_field": "location.display",
        "apply_url_prefix": "https://careers.google.com/jobs/results/",
        "region": "global",
        "entry_lpa": "25–50+",
    },

    "Microsoft": {
        "type": "api",
        "careers_url": "https://jobs.careers.microsoft.com/global/en/search?lc=India&d=Software%20Engineering",
        "api_url": "https://jobs.careers.microsoft.com/global/en/api/jobs?lc=India&exp=Experienced%20professionals&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true",
        "linkedin_search": "Microsoft Software Engineer India",
        "job_id_field": "jobId",
        "title_field": "title",
        "location_field": "primaryLocation",
        "apply_url_prefix": "https://jobs.careers.microsoft.com/global/en/job/",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "Amazon": {
        "type": "api",
        "careers_url": "https://www.amazon.jobs/en/search?base_query=software+engineer&loc_query=India",
        "api_url": "https://www.amazon.jobs/en/search.json?base_query=software+engineer&loc_query=India&job_count=20&result_limit=20&sort=relevant",
        "linkedin_search": "Amazon Software Engineer India",
        "job_id_field": "job_id",
        "title_field": "title",
        "location_field": "location",
        "apply_url_prefix": "https://www.amazon.jobs",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "Meta": {
        "type": "playwright",
        "careers_url": "https://www.metacareers.com/jobs?offices[0]=India&teams[0]=Software%20Engineering",
        "linkedin_search": "Meta Software Engineer India",
        "job_card_selector": "div[data-testid='job-listing']",
        "title_selector": "a[data-testid='job-listing-title']",
        "location_selector": "span[data-testid='job-listing-location']",
        "link_selector": "a[data-testid='job-listing-title']",
        "region": "global",
        "entry_lpa": "20–50",
    },

    "Apple": {
        "type": "playwright",
        "careers_url": "https://jobs.apple.com/en-us/search?location=india-IND&team=apps-and-frameworks-SFTWR-AF",
        "linkedin_search": "Apple Software Engineer India",
        "job_card_selector": "tbody tr",
        "title_selector": "td.table-col-1 a",
        "location_selector": "td.table-col-3",
        "link_selector": "td.table-col-1 a",
        "apply_url_prefix": "https://jobs.apple.com",
        "region": "global",
        "entry_lpa": "20–40",
    },

    "IBM": {
        "type": "playwright",
        "careers_url": "https://www.ibm.com/careers/search?field_keyword_08[0]=Software%20Engineering&field_keyword_18[0]=India",
        "linkedin_search": "IBM Software Engineer India",
        "job_card_selector": ".bx--tile",
        "title_selector": "h3",
        "location_selector": ".ibm--tile--location",
        "link_selector": "a",
        "region": "global",
        "entry_lpa": "10–18",
    },

    "Salesforce": {
        "type": "playwright",
        "careers_url": "https://careers.salesforce.com/en/jobs/?search=software+engineer&location=India",
        "linkedin_search": "Salesforce Software Engineer India",
        "job_card_selector": "li.jobs-list__item",
        "title_selector": "a.jobs-list__link",
        "location_selector": "span.location",
        "link_selector": "a.jobs-list__link",
        "apply_url_prefix": "https://careers.salesforce.com",
        "region": "global",
        "entry_lpa": "20–35",
    },

    "Adobe": {
        "type": "playwright",
        "careers_url": "https://careers.adobe.com/us/en/search-results?keywords=software%20engineer&location=India",
        "linkedin_search": "Adobe Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.adobe.com",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "SAP": {
        "type": "playwright",
        "careers_url": "https://jobs.sap.com/search/?q=software+engineer&locationsearch=India",
        "linkedin_search": "SAP Software Engineer India",
        "job_card_selector": "li.js-view-job",
        "title_selector": "h3.title a",
        "location_selector": "span.location",
        "link_selector": "h3.title a",
        "apply_url_prefix": "https://jobs.sap.com",
        "region": "global",
        "entry_lpa": "15–25",
    },

    "Oracle": {
        "type": "playwright",
        "careers_url": "https://careers.oracle.com/jobs/#en/sites/jobsearch/jobs?keyword=software+engineer&location=India",
        "linkedin_search": "Oracle Software Engineer India",
        "job_card_selector": "li.job",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.oracle.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "Atlassian": {
        "type": "playwright",
        "careers_url": "https://www.atlassian.com/company/careers/all-jobs?location=India&team=Engineering",
        "linkedin_search": "Atlassian Software Engineer India",
        "job_card_selector": "div[data-testid='job']",
        "title_selector": "a[data-testid='job-title']",
        "location_selector": "span[data-testid='job-location']",
        "link_selector": "a[data-testid='job-title']",
        "apply_url_prefix": "https://www.atlassian.com",
        "region": "global",
        "entry_lpa": "20–35",
    },

    "Nvidia": {
        "type": "playwright",
        "careers_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
        "linkedin_search": "Nvidia Software Engineer India",
        "job_card_selector": "li.JLQJ4429",
        "title_selector": "a.css-19uc56f",
        "location_selector": "dd.css-129m7dg",
        "link_selector": "a.css-19uc56f",
        "apply_url_prefix": "https://nvidia.wd5.myworkdayjobs.com",
        "region": "global",
        "ats": "workday",
        "entry_lpa": "17–30",
    },

    "Intel": {
        "type": "playwright",
        "careers_url": "https://jobs.intel.com/en/search-jobs/Software%20Engineer/India/599/1/2/6252001/39.26367/76.83617/100/1",
        "linkedin_search": "Intel Software Engineer India",
        "job_card_selector": "section.article--result",
        "title_selector": "h2 a",
        "location_selector": "span.job-location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.intel.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "Cisco": {
        "type": "playwright",
        "careers_url": "https://jobs.cisco.com/jobs/SearchJobs/software%20engineer?listFilterMode=1&locationCity=India",
        "linkedin_search": "Cisco Software Engineer India",
        "job_card_selector": "li.listSingleColumnItem",
        "title_selector": "h2 a",
        "location_selector": "span.jobLocation",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.cisco.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "ThoughtWorks": {
        "type": "playwright",
        "careers_url": "https://www.thoughtworks.com/careers/jobs?country=India",
        "linkedin_search": "ThoughtWorks Software Engineer India",
        "job_card_selector": "div.job-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.thoughtworks.com",
        "region": "global",
        "entry_lpa": "10–18",
    },

    "Samsung": {
        "type": "playwright",
        "careers_url": "https://samsung.com/us/careers/search/#q=software%20engineer&t=All&d=&l=India",
        "api_url": "https://sec-careers.samsungelectronics.com/en/api/jobs?keyword=software+engineer&location=India&size=20",
        "linkedin_search": "Samsung R&D Software Engineer India",
        "job_card_selector": "li.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "Qualcomm": {
        "type": "playwright",
        "careers_url": "https://careers.qualcomm.com/careers/search?keywords=software+engineer&location=India",
        "linkedin_search": "Qualcomm Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.qualcomm.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "AMD": {
        "type": "playwright",
        "careers_url": "https://careers.amd.com/careers-home/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "AMD Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.amd.com",
        "region": "global",
        "entry_lpa": "15–25",
    },

    "Texas Instruments": {
        "type": "playwright",
        "careers_url": "https://careers.ti.com/search/?q=software+engineer&locationsearch=India",
        "linkedin_search": "Texas Instruments Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.ti.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "Uber": {
        "type": "playwright",
        "careers_url": "https://www.uber.com/us/en/careers/list/?location=India&department=Engineering",
        "linkedin_search": "Uber Software Engineer India",
        "job_card_selector": "div[data-baseweb='block']",
        "title_selector": "h3",
        "location_selector": "span",
        "link_selector": "a",
        "apply_url_prefix": "https://www.uber.com",
        "region": "global",
        "entry_lpa": "20–35",
    },

    "Netflix": {
        "type": "playwright",
        "careers_url": "https://jobs.netflix.com/search?location=India&team=Engineering",
        "linkedin_search": "Netflix Software Engineer India",
        "job_card_selector": "div.css-1ul2x6m",
        "title_selector": "span.css-1hvhzl5",
        "location_selector": "span.css-1vdlgu6",
        "link_selector": "a",
        "apply_url_prefix": "https://jobs.netflix.com",
        "region": "global",
        "entry_lpa": "25–50",
    },

    "PayPal": {
        "type": "playwright",
        "careers_url": "https://careers.pypl.com/home/results/?searchkeyword=software+engineer&searchlocation=India",
        "linkedin_search": "PayPal Software Engineer India",
        "job_card_selector": "li.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.pypl.com",
        "region": "global",
        "entry_lpa": "12–20",
    },

    "Walmart": {
        "type": "playwright",
        "careers_url": "https://careers.walmart.com/results?q=software+engineer&location=India&job_type=Full-Time",
        "linkedin_search": "Walmart Labs Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.walmart.com",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "Zoom": {
        "type": "playwright",
        "careers_url": "https://careers.zoom.us/jobs/search?keywords=software+engineer&location=India",
        "linkedin_search": "Zoom Video Communications Software Engineer India",
        "job_card_selector": "li.css-1q2dra3",
        "title_selector": "a.css-19uc56f",
        "location_selector": "dd.css-129m7dg",
        "link_selector": "a.css-19uc56f",
        "apply_url_prefix": "https://careers.zoom.us",
        "region": "global",
        "ats": "workday",
        "entry_lpa": "20–35",
    },

    "LinkedIn": {
        "type": "playwright",
        "careers_url": "https://careers.linkedin.com/jobs/search?keywords=software+engineer&location=India",
        "linkedin_search": "LinkedIn Software Engineer India",
        "job_card_selector": "li.result-card",
        "title_selector": "a.result-card__full-card-link",
        "location_selector": "span.job-result-card__location",
        "link_selector": "a.result-card__full-card-link",
        "apply_url_prefix": "https://careers.linkedin.com",
        "region": "global",
        "entry_lpa": "44–67",
    },

    "Stripe": {
        "type": "playwright",
        "careers_url": "https://stripe.com/jobs/search?location=India&team=Engineering",
        "linkedin_search": "Stripe Software Engineer India",
        "job_card_selector": "div.JobsListings__item",
        "title_selector": "a.JobsListings__link",
        "location_selector": "span.JobsListings__location",
        "link_selector": "a.JobsListings__link",
        "apply_url_prefix": "https://stripe.com",
        "region": "global",
        "entry_lpa": "58–98",
    },

    "Booking.com": {
        "type": "playwright",
        "careers_url": "https://careers.booking.com/jobs/?keyword=software+engineer&location=India",
        "linkedin_search": "Booking.com Software Engineer India",
        "job_card_selector": "li.vacancies-list__item",
        "title_selector": "a.vacancies-list__link",
        "location_selector": "span.vacancies-list__location",
        "link_selector": "a.vacancies-list__link",
        "apply_url_prefix": "https://careers.booking.com",
        "region": "global",
        "entry_lpa": "25–40",
    },

    "Akamai Technologies": {
        "type": "playwright",
        "careers_url": "https://careers.akamai.com/careers/search?keywords=software+engineer&location=India",
        "linkedin_search": "Akamai Software Engineer India",
        "job_card_selector": "li.job-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.akamai.com",
        "region": "global",
        "entry_lpa": "20–28",
    },

    "AppDynamics": {
        "type": "playwright",
        "careers_url": "https://jobs.cisco.com/jobs/SearchJobs/AppDynamics?listFilterMode=1&locationCity=India",
        "linkedin_search": "AppDynamics Software Engineer India",
        "job_card_selector": "li.listSingleColumnItem",
        "title_selector": "h2 a",
        "location_selector": "span.jobLocation",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.cisco.com",
        "region": "global",
        "entry_lpa": "22–30",
        "notes": "AppDynamics is a Cisco subsidiary — jobs listed under Cisco careers portal.",
    },

    "Arista Networks": {
        "type": "playwright",
        "careers_url": "https://www.arista.com/en/careers/university/engineering?location=India",
        "linkedin_search": "Arista Networks Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.arista.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "ServiceNow": {
        "type": "playwright",
        "careers_url": "https://careers.servicenow.com/careers/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "ServiceNow Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.servicenow.com",
        "region": "global",
        "entry_lpa": "22–35",
    },

    "Twilio": {
        "type": "playwright",
        "careers_url": "https://twilio.com/en-us/company/jobs?q=software+engineer&location=India",
        "linkedin_search": "Twilio Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://twilio.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "Okta": {
        "type": "playwright",
        "careers_url": "https://www.okta.com/company/careers/?q=software+engineer&location=India",
        "linkedin_search": "Okta Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.okta.com",
        "region": "global",
        "entry_lpa": "20–28",
    },

    "Datadog": {
        "type": "playwright",
        "careers_url": "https://careers.datadoghq.com/all-jobs/?search=software+engineer&location=India",
        "linkedin_search": "Datadog Software Engineer India",
        "job_card_selector": "li.js-job",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.datadoghq.com",
        "region": "global",
        "entry_lpa": "22–35",
    },

    "Confluent": {
        "type": "playwright",
        "careers_url": "https://careers.confluent.io/jobs?search=software+engineer&location=India",
        "linkedin_search": "Confluent Software Engineer India",
        "job_card_selector": "li.opening",
        "title_selector": "a.opening-job-title",
        "location_selector": "span.location",
        "link_selector": "a.opening-job-title",
        "apply_url_prefix": "https://careers.confluent.io",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "HashiCorp": {
        "type": "playwright",
        "careers_url": "https://www.hashicorp.com/jobs/search?role=engineering&location=india",
        "linkedin_search": "HashiCorp Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.hashicorp.com",
        "region": "global",
        "entry_lpa": "20–28",
    },

    "GitLab": {
        "type": "requests",
        "careers_url": "https://about.gitlab.com/jobs/all-jobs/",
        "linkedin_search": "GitLab Software Engineer India",
        "job_card_selector": "div.job-row",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://about.gitlab.com",
        "region": "global",
        "entry_lpa": "20–30",
        "notes": "Fully remote — India-based applicants eligible for most engineering roles.",
    },

    # =========================================================================
    # SECTION 2: HFT / QUANT FIRMS  (NEW — Highest paying in India)
    # =========================================================================

    "Tower Research Capital": {
        "type": "requests",
        "careers_url": "https://tower-research.com/open-positions/",
        "linkedin_search": "Tower Research Capital Software Engineer India",
        "job_card_selector": "div.position-item",
        "title_selector": "a.position-title",
        "location_selector": "span.location",
        "link_selector": "a.position-title",
        "apply_url_prefix": "https://tower-research.com",
        "region": "hft_quant",
        "entry_lpa": "44–54",
        "notes": "India office in Gurgaon. Entry base ~30 LPA + 6L signing + 8–18L perf bonus. Requires strong DSA + C++.",
    },

    "Graviton Research Capital": {
        "type": "requests",
        "careers_url": "https://www.gravitontrading.com/careers.html",
        "linkedin_search": "Graviton Research Capital Software Engineer Bangalore",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.gravitontrading.com",
        "region": "hft_quant",
        "entry_lpa": "80–100+",
        "notes": "Bangalore. Among top 3 payers in India for freshers. Campus-first hiring from IITs. Very limited openings.",
    },

    "QuadEye Securities": {
        "type": "requests",
        "careers_url": "https://www.quadeye.com/careers/",
        "linkedin_search": "QuadEye Securities Software Engineer India",
        "job_card_selector": "div.career-opening",
        "title_selector": "h3.job-title",
        "location_selector": "span.location",
        "link_selector": "a",
        "apply_url_prefix": "https://www.quadeye.com",
        "region": "hft_quant",
        "entry_lpa": "58–95",
        "notes": "Delhi NCR. HFT prop trading firm. Extremely selective, IIT-focused campus hiring.",
    },

    "Quantbox Research": {
        "type": "requests",
        "careers_url": "https://www.quantbox.in/careers",
        "linkedin_search": "Quantbox Research Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "h3",
        "location_selector": "span.location",
        "link_selector": "a",
        "apply_url_prefix": "https://www.quantbox.in",
        "region": "hft_quant",
        "entry_lpa": "80–130+",
        "notes": "Top IIT campus placements at 80–130 LPA. Among highest domestic offers in India.",
    },

    "Optiver": {
        "type": "playwright",
        "careers_url": "https://optiver.com/working-at-optiver/career-opportunities/?location=india",
        "linkedin_search": "Optiver Software Engineer India",
        "job_card_selector": "li.vacancy-item",
        "title_selector": "a.vacancy-title",
        "location_selector": "span.vacancy-location",
        "link_selector": "a.vacancy-title",
        "apply_url_prefix": "https://optiver.com",
        "region": "hft_quant",
        "entry_lpa": "50–80",
        "notes": "Growing Bangalore presence. Amsterdam-HQ market maker and prop trading firm.",
    },

    "IMC Trading": {
        "type": "playwright",
        "careers_url": "https://www.imc.com/ap/careers/vacancies/?location=india",
        "linkedin_search": "IMC Trading Software Engineer India",
        "job_card_selector": "div.vacancy-card",
        "title_selector": "a.vacancy-title",
        "location_selector": "span.location",
        "link_selector": "a.vacancy-title",
        "apply_url_prefix": "https://www.imc.com",
        "region": "hft_quant",
        "entry_lpa": "40–70",
        "notes": "Offices in Bangalore and Mumbai. Global market-making and prop trading firm.",
    },

    "WorldQuant": {
        "type": "playwright",
        "careers_url": "https://www.worldquant.com/career-listing/?location=india",
        "linkedin_search": "WorldQuant Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.worldquant.com",
        "region": "hft_quant",
        "entry_lpa": "35–45",
        "notes": "Mumbai office. Quant hedge fund. Also runs BRAIN virtual research platform globally.",
    },

    "AlphaGrep": {
        "type": "requests",
        "careers_url": "https://alphagrep.com/careers",
        "linkedin_search": "AlphaGrep Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://alphagrep.com",
        "region": "hft_quant",
        "entry_lpa": "30–50",
        "notes": "Mumbai-based HFT prop trading firm. Selective hiring from top engineering colleges.",
    },

    # =========================================================================
    # SECTION 3: INDIAN IT SERVICES COMPANIES
    # =========================================================================

    "TCS": {
        "type": "playwright",
        "careers_url": "https://ibegin.tcs.com/iBegin/jobs/search?jobFunction=Software+Development&country=India",
        "linkedin_search": "TCS Software Engineer India",
        "job_card_selector": "div.job-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://ibegin.tcs.com",
        "region": "indian_it",
        "entry_lpa": "3.5–7",
    },

    "Infosys": {
        "type": "playwright",
        "careers_url": "https://career.infosys.com/joblist?companyhiringtype=IL&countrycode=IN&type=ALL",
        "linkedin_search": "Infosys Software Engineer India",
        "job_card_selector": "li.job-listing-item",
        "title_selector": ".job-title a",
        "location_selector": ".job-location",
        "link_selector": ".job-title a",
        "apply_url_prefix": "https://career.infosys.com",
        "region": "indian_it",
        "entry_lpa": "3.5–9",
    },

    "Wipro": {
        "type": "playwright",
        "careers_url": "https://careers.wipro.com/careers-home/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Wipro Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.wipro.com",
        "region": "indian_it",
        "entry_lpa": "3.5–6",
    },

    "HCL Tech": {
        "type": "playwright",
        "careers_url": "https://www.hcltech.com/careers/current-job-openings-in-india",
        "linkedin_search": "HCL Tech Software Engineer India",
        "job_card_selector": "tr.job-row",
        "title_selector": "td.job-title a",
        "location_selector": "td.job-location",
        "link_selector": "td.job-title a",
        "apply_url_prefix": "https://www.hcltech.com",
        "region": "indian_it",
        "entry_lpa": "3.5–7",
    },

    "Tech Mahindra": {
        "type": "playwright",
        "careers_url": "https://careers.techmahindra.com/jobs?q=software+engineer&l=India",
        "linkedin_search": "Tech Mahindra Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.techmahindra.com",
        "region": "indian_it",
        "entry_lpa": "3.5–6",
    },

    "Cognizant": {
        "type": "playwright",
        "careers_url": "https://careers.cognizant.com/global/en/search-results?keywords=software+engineer&selected_location=India",
        "linkedin_search": "Cognizant Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.cognizant.com",
        "region": "indian_it",
        "entry_lpa": "3.5–6",
    },

    "Hexaware": {
        "type": "playwright",
        "careers_url": "https://hexaware.com/careers/?s=software+engineer&country=India",
        "linkedin_search": "Hexaware Software Engineer India",
        "job_card_selector": "article.job-post",
        "title_selector": "h2 a",
        "location_selector": "span.location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://hexaware.com",
        "region": "indian_it",
        "entry_lpa": "4–8",
    },

    "Mphasis": {
        "type": "playwright",
        "careers_url": "https://careers.mphasis.com/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Mphasis Software Engineer India",
        "job_card_selector": "li.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.mphasis.com",
        "region": "indian_it",
        "entry_lpa": "4–8",
    },

    "LTIMindtree": {
        "type": "playwright",
        "careers_url": "https://www.ltimindtree.com/careers/jobs/?keyword=software+engineer&location=India",
        "linkedin_search": "LTIMindtree Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.ltimindtree.com",
        "region": "indian_it",
        "entry_lpa": "4–8",
    },

    "Persistent Systems": {
        "type": "playwright",
        "careers_url": "https://careers.persistent.com/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Persistent Systems Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.persistent.com",
        "region": "indian_it",
        "entry_lpa": "5–10",
    },

    "Coforge": {
        "type": "playwright",
        "careers_url": "https://www.coforge.com/careers/current-openings?keyword=software+engineer&location=India",
        "linkedin_search": "Coforge Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.coforge.com",
        "region": "indian_it",
        "entry_lpa": "4–8",
    },

    "Birlasoft": {
        "type": "playwright",
        "careers_url": "https://www.birlasoft.com/careers/current-openings?search=software+engineer",
        "linkedin_search": "Birlasoft Software Engineer India",
        "job_card_selector": "div.career-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.birlasoft.com",
        "region": "indian_it",
        "entry_lpa": "4–7",
    },

    "Zensar Technologies": {
        "type": "playwright",
        "careers_url": "https://careers.zensar.com/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Zensar Software Engineer India",
        "job_card_selector": "li.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.zensar.com",
        "region": "indian_it",
        "entry_lpa": "4–7",
    },

    "Happiest Minds": {
        "type": "playwright",
        "careers_url": "https://www.happiestminds.com/careers/current-opening/?s=software+engineer",
        "linkedin_search": "Happiest Minds Software Engineer India",
        "job_card_selector": "div.opening-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.happiestminds.com",
        "region": "indian_it",
        "entry_lpa": "4–8",
    },

    "Nagarro": {
        "type": "playwright",
        "careers_url": "https://www.nagarro.com/en/careers/open-positions?keyword=software+engineer&location=India",
        "linkedin_search": "Nagarro Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.nagarro.com",
        "region": "indian_it",
        "entry_lpa": "5–10",
    },

    # =========================================================================
    # SECTION 4: MNC IT SERVICES & CONSULTING
    # =========================================================================

    "Accenture": {
        "type": "playwright",
        "careers_url": "https://www.accenture.com/us-en/careers/jobsearch?jk=software+engineer&il=India&pg=1",
        "linkedin_search": "Accenture Software Engineer India",
        "job_card_selector": "li.cmp-job-listing-item",
        "title_selector": "a.cmp-job-listing-item__title",
        "location_selector": "span.cmp-job-listing-item__location",
        "link_selector": "a.cmp-job-listing-item__title",
        "apply_url_prefix": "https://www.accenture.com",
        "region": "mnc_services",
        "entry_lpa": "4–9",
    },

    "Deloitte": {
        "type": "playwright",
        "careers_url": "https://apply.deloitte.com/careers/SearchJobs/software%20engineer?3_56_3=224",
        "linkedin_search": "Deloitte Software Engineer India",
        "job_card_selector": "li.listSingleColumnItem",
        "title_selector": "h2 a",
        "location_selector": "span.jobLocation",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://apply.deloitte.com",
        "region": "mnc_services",
        "entry_lpa": "6–12",
    },

    "Capgemini": {
        "type": "playwright",
        "careers_url": "https://www.capgemini.com/jobs/search-jobs/?search_api_fulltext=software+engineer&field_job_country=india",
        "linkedin_search": "Capgemini Software Engineer India",
        "job_card_selector": "article.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.capgemini.com",
        "region": "mnc_services",
        "entry_lpa": "4–8",
    },

    "Publicis Sapient": {
        "type": "playwright",
        "careers_url": "https://jobs.publicissapient.com/jobs?q=software+engineer&l=India",
        "linkedin_search": "Publicis Sapient Software Engineer India",
        "job_card_selector": "div.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://jobs.publicissapient.com",
        "region": "mnc_services",
        "entry_lpa": "8–15",
    },

    "Genpact": {
        "type": "playwright",
        "careers_url": "https://www.genpact.com/careers/open-positions?title=software+engineer&location=India",
        "linkedin_search": "Genpact Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.genpact.com",
        "region": "mnc_services",
        "entry_lpa": "4–8",
    },

    "EXL Analytics": {
        "type": "playwright",
        "careers_url": "https://careers.exlservice.com/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "EXL Analytics Software Engineer India",
        "job_card_selector": "li.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.exlservice.com",
        "region": "mnc_services",
        "entry_lpa": "5–10",
    },

    # =========================================================================
    # SECTION 5: INDIAN UNICORNS & HIGH-GROWTH STARTUPS
    # =========================================================================

    "Flipkart": {
        "type": "playwright",
        "careers_url": "https://www.flipkartcareers.com/#!/joblist?jobQuery=software+engineer",
        "linkedin_search": "Flipkart Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.flipkartcareers.com",
        "region": "indian_unicorn",
        "entry_lpa": "17–25",
    },

    "Zomato": {
        "type": "playwright",
        "careers_url": "https://www.zomato.com/careers#jobs?job_type=Technology&location=India",
        "linkedin_search": "Zomato Software Engineer India",
        "job_card_selector": "div[data-testid='job-card']",
        "title_selector": "a[data-testid='job-title']",
        "location_selector": "span[data-testid='job-location']",
        "link_selector": "a[data-testid='job-title']",
        "apply_url_prefix": "https://www.zomato.com",
        "region": "indian_unicorn",
        "entry_lpa": "17–25",
    },

    "Swiggy": {
        "type": "playwright",
        "careers_url": "https://careers.swiggy.com/#/careers?domain=Engineering",
        "linkedin_search": "Swiggy Software Engineer India",
        "job_card_selector": "div.career-card",
        "title_selector": "a.career-title",
        "location_selector": "span.location",
        "link_selector": "a.career-title",
        "apply_url_prefix": "https://careers.swiggy.com",
        "region": "indian_unicorn",
        "entry_lpa": "17–25",
    },

    "PhonePe": {
        "type": "playwright",
        "careers_url": "https://www.phonepe.com/careers/?department=Engineering",
        "linkedin_search": "PhonePe Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.phonepe.com",
        "region": "indian_unicorn",
        "entry_lpa": "15–25",
    },

    "Razorpay": {
        "type": "playwright",
        "careers_url": "https://razorpay.com/jobs/?department=Engineering",
        "linkedin_search": "Razorpay Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://razorpay.com",
        "region": "indian_unicorn",
        "entry_lpa": "15–25",
    },

    "Meesho": {
        "type": "playwright",
        "careers_url": "https://www.meesho.io/jobs?department=Engineering",
        "linkedin_search": "Meesho Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.meesho.io",
        "region": "indian_unicorn",
        "entry_lpa": "15–22",
    },

    "Zerodha": {
        "type": "requests",
        "careers_url": "https://careers.zerodha.com/",
        "linkedin_search": "Zerodha Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "h3.job-title",
        "location_selector": "span.location",
        "link_selector": "a",
        "apply_url_prefix": "https://careers.zerodha.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "CRED": {
        "type": "playwright",
        "careers_url": "https://careers.cred.club/?department=Engineering",
        "linkedin_search": "CRED Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.cred.club",
        "region": "indian_unicorn",
        "entry_lpa": "15–25",
    },

    "Groww": {
        "type": "playwright",
        "careers_url": "https://careers.groww.in/openings?department=Engineering",
        "linkedin_search": "Groww Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.groww.in",
        "region": "indian_unicorn",
        "entry_lpa": "15–22",
    },

    "Nykaa": {
        "type": "playwright",
        "careers_url": "https://jobs.nykaa.com/search/?q=software+engineer",
        "linkedin_search": "Nykaa Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "h2 a",
        "location_selector": "span.location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.nykaa.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "Freshworks": {
        "type": "playwright",
        "careers_url": "https://www.freshworks.com/company/careers/openings/?department=Engineering",
        "linkedin_search": "Freshworks Software Engineer India",
        "job_card_selector": "div.open-positions__item",
        "title_selector": "a.position-title",
        "location_selector": "span.location",
        "link_selector": "a.position-title",
        "apply_url_prefix": "https://www.freshworks.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–20",
    },

    "ShareChat": {
        "type": "playwright",
        "careers_url": "https://careers.sharechat.com/openings?department=Engineering",
        "linkedin_search": "ShareChat Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.sharechat.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–30",
    },

    "OYO": {
        "type": "playwright",
        "careers_url": "https://jobs.oyorooms.com/?department=Technology&location=India",
        "linkedin_search": "OYO Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://jobs.oyorooms.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "Delhivery": {
        "type": "playwright",
        "careers_url": "https://www.delhivery.com/careers?department=Technology&location=India",
        "linkedin_search": "Delhivery Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.delhivery.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "Ola": {
        "type": "playwright",
        "careers_url": "https://www.olacabs.com/careers?department=Engineering&location=India",
        "linkedin_search": "Ola Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.olacabs.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–20",
    },

    "Jio Platforms": {
        "type": "playwright",
        "careers_url": "https://careers.jio.com/search-jobs?q=software+engineer",
        "linkedin_search": "Jio Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.jio.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "Paytm": {
        "type": "playwright",
        "careers_url": "https://paytm.com/about-us/careers?department=Engineering",
        "linkedin_search": "Paytm Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://paytm.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "Urban Company": {
        "type": "playwright",
        "careers_url": "https://www.urbancompany.com/careers?team=Engineering",
        "linkedin_search": "Urban Company Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.urbancompany.com",
        "region": "indian_unicorn",
        "entry_lpa": "15–22",
    },

    "Unacademy": {
        "type": "playwright",
        "careers_url": "https://unacademy.com/careers?department=Engineering",
        "linkedin_search": "Unacademy Software Engineer India",
        "job_card_selector": "div.career-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://unacademy.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "InMobi": {
        "type": "playwright",
        "careers_url": "https://www.inmobi.com/company/careers/?department=Engineering",
        "linkedin_search": "InMobi Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.inmobi.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–30",
    },

    "MakeMyTrip": {
        "type": "playwright",
        "careers_url": "https://careers.makemytrip.com/jobs?department=Technology",
        "linkedin_search": "MakeMyTrip Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.makemytrip.com",
        "region": "indian_unicorn",
        "entry_lpa": "10–18",
    },

    "BrowserStack": {
        "type": "playwright",
        "careers_url": "https://www.browserstack.com/careers#open-positions?department=Engineering",
        "linkedin_search": "BrowserStack Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.browserstack.com",
        "region": "indian_unicorn",
        "entry_lpa": "15–22",
    },

    "Juspay": {
        "type": "playwright",
        "careers_url": "https://juspay.in/careers",
        "linkedin_search": "Juspay Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://juspay.in",
        "region": "indian_unicorn",
        "entry_lpa": "20–30",
    },

    "Chargebee": {
        "type": "playwright",
        "careers_url": "https://www.chargebee.com/careers/?department=Engineering",
        "linkedin_search": "Chargebee Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.chargebee.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–28",
    },

    "Druva": {
        "type": "playwright",
        "careers_url": "https://www.druva.com/company/careers/?department=Engineering&location=India",
        "linkedin_search": "Druva Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.druva.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–30",
    },

    "Darwinbox": {
        "type": "playwright",
        "careers_url": "https://darwinbox.com/careers?department=Engineering",
        "linkedin_search": "Darwinbox Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://darwinbox.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–25",
    },

    "CleverTap": {
        "type": "playwright",
        "careers_url": "https://clevertap.com/company/careers/?department=Engineering",
        "linkedin_search": "CleverTap Software Engineer India",
        "job_card_selector": "div.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://clevertap.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–25",
    },

    "MoEngage": {
        "type": "playwright",
        "careers_url": "https://www.moengage.com/about/careers/?department=Engineering",
        "linkedin_search": "MoEngage Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.moengage.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–25",
    },

    "Innovaccer": {
        "type": "playwright",
        "careers_url": "https://innovaccer.com/company/careers/?department=Engineering",
        "linkedin_search": "Innovaccer Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://innovaccer.com",
        "region": "indian_unicorn",
        "entry_lpa": "20–28",
    },

    "Samsara": {
        "type": "playwright",
        "careers_url": "https://www.samsara.com/company/careers/?department=Engineering&location=India",
        "linkedin_search": "Samsara Software Engineer India",
        "job_card_selector": "li.opening",
        "title_selector": "a.opening-job-title",
        "location_selector": "span.location",
        "link_selector": "a.opening-job-title",
        "apply_url_prefix": "https://www.samsara.com",
        "region": "indian_unicorn",
        "entry_lpa": "22–35",
    },

    # =========================================================================
    # SECTION 6: CLOUD / DEVTOOLS / SAAS
    # =========================================================================

    "Databricks": {
        "type": "playwright",
        "careers_url": "https://www.databricks.com/company/careers/open-positions?department=Engineering&location=India",
        "linkedin_search": "Databricks Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.databricks.com",
        "region": "global",
        "entry_lpa": "25–40",
    },

    "Snowflake": {
        "type": "playwright",
        "careers_url": "https://careers.snowflake.com/us/en/search-results?keywords=software+engineer&location=India",
        "linkedin_search": "Snowflake Software Engineer India",
        "job_card_selector": "li.jobs-list-item",
        "title_selector": "a.job-title",
        "location_selector": "span.job-location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.snowflake.com",
        "region": "global",
        "entry_lpa": "20–35",
    },

    "MongoDB": {
        "type": "playwright",
        "careers_url": "https://www.mongodb.com/careers/jobs?department=Engineering&location=India",
        "linkedin_search": "MongoDB Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.mongodb.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "Palo Alto Networks": {
        "type": "playwright",
        "careers_url": "https://jobs.paloaltonetworks.com/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Palo Alto Networks Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://jobs.paloaltonetworks.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "CrowdStrike": {
        "type": "playwright",
        "careers_url": "https://crowdstrike.wd5.myworkdayjobs.com/crowdstrikecareers?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
        "linkedin_search": "CrowdStrike Software Engineer India",
        "job_card_selector": "li.JLQJ4429",
        "title_selector": "a.css-19uc56f",
        "location_selector": "dd.css-129m7dg",
        "link_selector": "a.css-19uc56f",
        "apply_url_prefix": "https://crowdstrike.wd5.myworkdayjobs.com",
        "region": "global",
        "ats": "workday",
        "entry_lpa": "20–30",
    },

    "Nutanix": {
        "type": "playwright",
        "careers_url": "https://nutanix.jobs/jobs?keywords=software+engineer&location=India",
        "linkedin_search": "Nutanix Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "h2 a",
        "location_selector": "span.location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://nutanix.jobs",
        "region": "global",
        "entry_lpa": "17–25",
    },

    "Rubrik": {
        "type": "playwright",
        "careers_url": "https://www.rubrik.com/company/careers/departments/engineering?location=India",
        "linkedin_search": "Rubrik Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.rubrik.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "Sprinklr": {
        "type": "playwright",
        "careers_url": "https://www.sprinklr.com/careers/open-positions/?department=Engineering&location=India",
        "linkedin_search": "Sprinklr Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.sprinklr.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "Postman": {
        "type": "playwright",
        "careers_url": "https://www.postman.com/company/careers/?department=Engineering",
        "linkedin_search": "Postman Software Engineer India",
        "job_card_selector": "div.job-listing",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.postman.com",
        "region": "global",
        "entry_lpa": "20–30",
    },

    "Pure Storage": {
        "type": "playwright",
        "careers_url": "https://boards.greenhouse.io/purestorage?gh_src=&q=software+engineer&location=India",
        "linkedin_search": "Pure Storage Software Engineer India",
        "job_card_selector": "div.opening",
        "title_selector": "a.opening-job-title",
        "location_selector": "span.location",
        "link_selector": "a.opening-job-title",
        "apply_url_prefix": "https://boards.greenhouse.io",
        "region": "global",
        "ats": "greenhouse",
        "entry_lpa": "20–30",
        "notes": "India office in Bangalore. Uses Greenhouse ATS. Fresher avg ~20.79 LPA base; median SWE total comp ~85 LPA. Rebranded as Everpure in 2025 but engineering jobs still posted under Pure Storage on Greenhouse.",
    },

    "Cohesity": {
        "type": "playwright",
        "careers_url": "https://www.cohesity.com/company/careers/open-positions/?keyword=software+engineer&location=India",
        "linkedin_search": "Cohesity Software Engineer India",
        "job_card_selector": "div.opening",
        "title_selector": "a.opening-job-title",
        "location_selector": "span.location",
        "link_selector": "a.opening-job-title",
        "apply_url_prefix": "https://www.cohesity.com",
        "region": "global",
        "ats": "greenhouse",
        "entry_lpa": "27–40",
        "notes": "India office in Bangalore. Entry-level starts ~27 LPA — 46% above industry avg. Median SWE total comp in Bengaluru ~75 LPA. Backed by NVIDIA, IBM, HPE, Cisco, AWS, Google Cloud. Hires heavily from IITs and BITS Pilani.",
    },

    # =========================================================================
    # SECTION 7: FINANCE / BANKING TECH  (NEW — all 20+ LPA at entry)
    # =========================================================================

    "Goldman Sachs": {
        "type": "playwright",
        "careers_url": "https://www.goldmansachs.com/careers/professionals/find-a-role/index.html?program=&region=India&office=&skills=Software+Engineering",
        "linkedin_search": "Goldman Sachs Software Engineer India",
        "job_card_selector": "li.js-insight",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.goldmansachs.com",
        "region": "finance_tech",
        "entry_lpa": "20–35",
    },

    "Morgan Stanley": {
        "type": "playwright",
        "careers_url": "https://www.morganstanley.com/careers/career-opportunities-search?keyword=software+engineer&location=India",
        "linkedin_search": "Morgan Stanley Software Engineer India",
        "job_card_selector": "li.job-posting",
        "title_selector": "a",
        "location_selector": "span.location",
        "link_selector": "a",
        "apply_url_prefix": "https://www.morganstanley.com",
        "region": "finance_tech",
        "entry_lpa": "20–35",
    },

    "JP Morgan": {
        "type": "playwright",
        "careers_url": "https://careers.jpmorgan.com/us/en/jobs?search=software+engineer&location=India",
        "linkedin_search": "JP Morgan Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "h2 a",
        "location_selector": "span.location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://careers.jpmorgan.com",
        "region": "finance_tech",
        "entry_lpa": "20–35",
    },

    "Deutsche Bank": {
        "type": "playwright",
        "careers_url": "https://careers.db.com/professionals/search-roles/#/professionals?lat=20.593684&lng=78.96288&loc=India&orRadius=200&page=1&search=software+engineer",
        "linkedin_search": "Deutsche Bank Software Engineer India",
        "job_card_selector": "li.db-js-item",
        "title_selector": "a.job-listing__title",
        "location_selector": "span.job-listing__location",
        "link_selector": "a.job-listing__title",
        "apply_url_prefix": "https://careers.db.com",
        "region": "finance_tech",
        "entry_lpa": "18–28",
    },

    "DE Shaw": {
        "type": "playwright",
        "careers_url": "https://www.deshaw.com/careers/search?query=software+engineer&location=India",
        "linkedin_search": "DE Shaw Software Engineer India",
        "job_card_selector": "div.career-item",
        "title_selector": "a.career-title",
        "location_selector": "span.location",
        "link_selector": "a.career-title",
        "apply_url_prefix": "https://www.deshaw.com",
        "region": "finance_tech",
        "entry_lpa": "20–35",
    },

    "Arcesium": {
        "type": "playwright",
        "careers_url": "https://www.arcesium.com/careers/?department=Technology&location=India",
        "linkedin_search": "Arcesium Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.arcesium.com",
        "region": "finance_tech",
        "entry_lpa": "17–25",
    },

    "Barclays": {
        "type": "playwright",
        "careers_url": "https://search.jobs.barclays/india/results?keywords=software+engineer",
        "linkedin_search": "Barclays Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://search.jobs.barclays",
        "region": "finance_tech",
        "entry_lpa": "20–30",
    },

    "HSBC Technology": {
        "type": "playwright",
        "careers_url": "https://www.hsbc.com/careers/jobs?search=software+engineer&country=India",
        "linkedin_search": "HSBC Technology Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://www.hsbc.com",
        "region": "finance_tech",
        "entry_lpa": "20–28",
    },

    "American Express": {
        "type": "playwright",
        "careers_url": "https://aexp.com/careers/jobs?q=software+engineer&location=India",
        "linkedin_search": "American Express Software Engineer India",
        "job_card_selector": "li.job-item",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://aexp.com",
        "region": "finance_tech",
        "entry_lpa": "20–28",
    },

    "Visa": {
        "type": "playwright",
        "careers_url": "https://careers.visa.com/jobs/search?q=software+engineer&l=India",
        "linkedin_search": "Visa Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.visa.com",
        "region": "finance_tech",
        "entry_lpa": "20–28",
    },

    "BlackRock": {
        "type": "playwright",
        "careers_url": "https://careers.blackrock.com/job-search-results/?keyword=software+engineer&location=India",
        "linkedin_search": "BlackRock Software Engineer India",
        "job_card_selector": "li.job-result",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://careers.blackrock.com",
        "region": "finance_tech",
        "entry_lpa": "22–35",
    },

    "BNY Mellon": {
        "type": "playwright",
        "careers_url": "https://bnymellon.com/us/en/careers/job-search.html#q=software+engineer&l=India",
        "linkedin_search": "BNY Mellon Software Engineer India",
        "job_card_selector": "div.job-card",
        "title_selector": "a.job-title",
        "location_selector": "span.location",
        "link_selector": "a.job-title",
        "apply_url_prefix": "https://bnymellon.com",
        "region": "finance_tech",
        "entry_lpa": "20–26",
    },

    "Citi": {
        "type": "playwright",
        "careers_url": "https://jobs.citi.com/search-jobs/software%20engineer/India/287/1/2/6252001/39.26367/76.83617/100/1",
        "linkedin_search": "Citi Software Engineer India",
        "job_card_selector": "section.article--result",
        "title_selector": "h2 a",
        "location_selector": "span.job-location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.citi.com",
        "region": "finance_tech",
        "entry_lpa": "20–30",
    },

    "Standard Chartered": {
        "type": "playwright",
        "careers_url": "https://scb.taleo.net/careersection/ex/jobsearch.ftl?lang=en&location=IND&keyword=software+engineer",
        "linkedin_search": "Standard Chartered Software Engineer India",
        "job_card_selector": "tr.job",
        "title_selector": "a.jobTitle",
        "location_selector": "span.location",
        "link_selector": "a.jobTitle",
        "apply_url_prefix": "https://scb.taleo.net",
        "region": "finance_tech",
        "entry_lpa": "20–25",
    },

    "Fidelity Investments": {
        "type": "playwright",
        "careers_url": "https://jobs.fidelity.com/search-jobs/software+engineer/India/11362/1/2/6252001/39.26367/76.83617/100/1",
        "linkedin_search": "Fidelity Investments Software Engineer India",
        "job_card_selector": "section.article--result",
        "title_selector": "h2 a",
        "location_selector": "span.job-location",
        "link_selector": "h2 a",
        "apply_url_prefix": "https://jobs.fidelity.com",
        "region": "finance_tech",
        "entry_lpa": "20–30",
    },

}


# =============================================================================
#  HELPER GROUPINGS — used by main.py and telegram_bot.py
# =============================================================================

INDIAN_IT_COMPANIES = [
    "TCS", "Infosys", "Wipro", "HCL Tech", "Tech Mahindra",
    "Cognizant", "Hexaware", "Mphasis", "LTIMindtree", "Persistent Systems",
    "Coforge", "Birlasoft", "Zensar Technologies", "Happiest Minds", "Nagarro",
]

GLOBAL_TECH_COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "IBM",
    "Salesforce", "Adobe", "SAP", "Oracle", "Atlassian", "Nvidia",
    "Intel", "Cisco", "ThoughtWorks", "Samsung", "Qualcomm", "AMD",
    "Texas Instruments", "Uber", "Netflix", "PayPal", "Walmart", "Zoom",
    "LinkedIn", "Stripe", "Booking.com", "Akamai Technologies",
    "AppDynamics", "Arista Networks", "ServiceNow", "Twilio", "Okta",
    "Datadog", "Confluent", "HashiCorp", "GitLab",
    "Databricks", "Snowflake", "MongoDB", "Palo Alto Networks", "CrowdStrike",
    "Nutanix", "Rubrik", "Sprinklr", "Postman", "Pure Storage", "Cohesity",
]

HFT_QUANT_COMPANIES = [
    "Tower Research Capital", "Graviton Research Capital", "QuadEye Securities",
    "Quantbox Research", "Optiver", "IMC Trading", "WorldQuant", "AlphaGrep",
]

INDIAN_UNICORN_COMPANIES = [
    "Flipkart", "Zomato", "Swiggy", "PhonePe", "Razorpay",
    "Meesho", "Zerodha", "CRED", "Groww", "Nykaa",
    "Freshworks", "ShareChat", "OYO", "Delhivery", "Ola",
    "Jio Platforms", "Paytm", "Urban Company", "Unacademy", "InMobi",
    "MakeMyTrip", "BrowserStack", "Juspay", "Chargebee", "Druva",
    "Darwinbox", "CleverTap", "MoEngage", "Innovaccer", "Samsara",
]

MNC_SERVICES_COMPANIES = [
    "Accenture", "Deloitte", "Capgemini", "Publicis Sapient",
    "Genpact", "EXL Analytics",
]

FINANCE_TECH_COMPANIES = [
    "Goldman Sachs", "Morgan Stanley", "JP Morgan", "Deutsche Bank",
    "DE Shaw", "Arcesium", "Barclays", "HSBC Technology",
    "American Express", "Visa", "BlackRock", "BNY Mellon",
    "Citi", "Standard Chartered", "Fidelity Investments",
]

# All companies in one flat list (for iteration in main.py)
ALL_COMPANIES = (
    INDIAN_IT_COMPANIES
    + GLOBAL_TECH_COMPANIES
    + HFT_QUANT_COMPANIES
    + INDIAN_UNICORN_COMPANIES
    + MNC_SERVICES_COMPANIES
    + FINANCE_TECH_COMPANIES
)

# Subset: only companies paying 20+ LPA at entry level (for premium digest mode)
HIGH_PAY_COMPANIES = [
    # HFT / Quant
    "Tower Research Capital", "Graviton Research Capital", "QuadEye Securities",
    "Quantbox Research", "Optiver", "IMC Trading", "WorldQuant", "AlphaGrep",
    # Global Tech
    "Google", "Meta", "Netflix", "Stripe", "LinkedIn", "Salesforce",
    "Atlassian", "Uber", "Databricks", "Snowflake", "ServiceNow",
    "Datadog", "Booking.com", "Rubrik", "Sprinklr", "CrowdStrike",
    "MongoDB", "Palo Alto Networks", "Zoom", "Akamai Technologies",
    "AppDynamics", "Arista Networks", "Twilio", "Okta", "Confluent",
    "HashiCorp", "GitLab", "Pure Storage", "Cohesity",
    # Finance
    "Goldman Sachs", "Morgan Stanley", "JP Morgan", "DE Shaw",
    "BlackRock", "Barclays", "HSBC Technology", "American Express",
    "Visa", "BNY Mellon", "Citi", "Standard Chartered", "Fidelity Investments",
    # Indian Unicorns
    "ShareChat", "InMobi", "Juspay", "Chargebee", "Druva",
    "Darwinbox", "CleverTap", "MoEngage", "Innovaccer", "Samsara",
    "Flipkart", "Zomato", "Swiggy", "PhonePe", "Razorpay",
    "CRED", "Urban Company", "BrowserStack",
]


# =============================================================================
#  SECTION 8: NEWLY DISCOVERED COMPANIES
#  Source: Cross-referenced from GitHub gist (322 companies), IIT placement
#  reports (IITB/IITD/IITM/IITKGP 2024), Levels.fyi India leaderboard,
#  Blind/Glassdoor research. Only companies appearing in 2+ sources added.
#  All pay 15+ LPA at entry level unless noted.
# =============================================================================

# ── EDA / Semiconductor Design Tools ─────────────────────────────────────────

COMPANY_CONFIGS["Cadence"] = {
    "type": "playwright",
    "careers_url": "https://cadence.wd1.myworkdayjobs.com/External_Careers?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
    "linkedin_search": "Cadence Design Systems Software Engineer India",
    "job_card_selector": "li.JLQJ4429",
    "title_selector": "a.css-19uc56f",
    "location_selector": "dd.css-129m7dg",
    "link_selector": "a.css-19uc56f",
    "apply_url_prefix": "https://cadence.wd1.myworkdayjobs.com",
    "region": "global",
    "ats": "workday",
    "entry_lpa": "15–25",
    "notes": "EDA tools. Offices in Bangalore, Noida, Hyderabad. Consistent IIT recruiter.",
}

COMPANY_CONFIGS["Synopsys"] = {
    "type": "playwright",
    "careers_url": "https://synopsys.avature.net/careers/SearchJobs?locationIdList=1243&projectOffset=0",
    "linkedin_search": "Synopsys Software Engineer India",
    "job_card_selector": "li.article--result",
    "title_selector": "h2 a",
    "location_selector": "span.job-location",
    "link_selector": "h2 a",
    "apply_url_prefix": "https://synopsys.avature.net",
    "region": "global",
    "entry_lpa": "15–25",
    "notes": "EDA/chip design tools. Bangalore, Hyderabad, Noida offices.",
}

COMPANY_CONFIGS["KLA"] = {
    "type": "playwright",
    "careers_url": "https://kla.wd1.myworkdayjobs.com/Search?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
    "linkedin_search": "KLA Corporation Software Engineer India",
    "job_card_selector": "li.JLQJ4429",
    "title_selector": "a.css-19uc56f",
    "location_selector": "dd.css-129m7dg",
    "link_selector": "a.css-19uc56f",
    "apply_url_prefix": "https://kla.wd1.myworkdayjobs.com",
    "region": "global",
    "ats": "workday",
    "entry_lpa": "15–28",
    "notes": "Semiconductor process equipment. Bangalore office. Day 1 IIT recruiter.",
}

COMPANY_CONFIGS["Ansys"] = {
    "type": "playwright",
    "careers_url": "https://careers.ansys.com/jobs?location=India&keywords=software+engineer",
    "linkedin_search": "Ansys Software Engineer India",
    "job_card_selector": "li.job-result",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.ansys.com",
    "region": "global",
    "entry_lpa": "12–22",
    "notes": "Simulation software. Pune and Bangalore offices.",
}

COMPANY_CONFIGS["MathWorks"] = {
    "type": "playwright",
    "careers_url": "https://www.mathworks.com/company/jobs/opportunities/search?q=software+engineer&location=India",
    "linkedin_search": "MathWorks Software Engineer India",
    "job_card_selector": "div.job-listing",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.mathworks.com",
    "region": "global",
    "entry_lpa": "15–25",
    "notes": "MATLAB/Simulink maker. Hyderabad office. Consistent IIT campus recruiter.",
}

COMPANY_CONFIGS["Autodesk"] = {
    "type": "playwright",
    "careers_url": "https://autodesk.wd1.myworkdayjobs.com/Ext?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
    "linkedin_search": "Autodesk Software Engineer India",
    "job_card_selector": "li.JLQJ4429",
    "title_selector": "a.css-19uc56f",
    "location_selector": "dd.css-129m7dg",
    "link_selector": "a.css-19uc56f",
    "apply_url_prefix": "https://autodesk.wd1.myworkdayjobs.com",
    "region": "global",
    "ats": "workday",
    "entry_lpa": "15–25",
    "notes": "CAD/design software. Bangalore and Hyderabad offices.",
}

# ── Storage / Data Management ─────────────────────────────────────────────────

COMPANY_CONFIGS["Western Digital"] = {
    "type": "playwright",
    "careers_url": "https://jobs.westerndigital.com/jobs?location=India&keywords=software+engineer",
    "linkedin_search": "Western Digital Software Engineer India",
    "job_card_selector": "li.job-result",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://jobs.westerndigital.com",
    "region": "global",
    "entry_lpa": "12–22",
    "notes": "Flash & HDD storage. Bangalore office (large). Regular campus recruiter.",
}

COMPANY_CONFIGS["NetApp"] = {
    "type": "playwright",
    "careers_url": "https://netapp.wd1.myworkdayjobs.com/External?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
    "linkedin_search": "NetApp Software Engineer India",
    "job_card_selector": "li.JLQJ4429",
    "title_selector": "a.css-19uc56f",
    "location_selector": "dd.css-129m7dg",
    "link_selector": "a.css-19uc56f",
    "apply_url_prefix": "https://netapp.wd1.myworkdayjobs.com",
    "region": "global",
    "ats": "workday",
    "entry_lpa": "15–25",
    "notes": "Cloud data management. Bangalore and Pune offices. IIT campus recruiter.",
}

COMPANY_CONFIGS["Broadcom"] = {
    "type": "playwright",
    "careers_url": "https://careers.broadcom.com/jobs?location=India&keywords=software+engineer",
    "linkedin_search": "Broadcom Software Engineer India",
    "job_card_selector": "li.job-result",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.broadcom.com",
    "region": "global",
    "entry_lpa": "15–25",
    "notes": "Semiconductor and infrastructure software. Bangalore, Hyderabad offices.",
}

COMPANY_CONFIGS["Commvault"] = {
    "type": "playwright",
    "careers_url": "https://careers.commvault.com/jobs?location=India&keywords=software+engineer",
    "linkedin_search": "Commvault Software Engineer India",
    "job_card_selector": "li.job-result",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.commvault.com",
    "region": "global",
    "entry_lpa": "15–22",
    "notes": "Data protection & backup. Hyderabad office.",
}

# ── Fintech / Finance SaaS ────────────────────────────────────────────────────

COMPANY_CONFIGS["Intuit"] = {
    "type": "playwright",
    "careers_url": "https://jobs.intuit.com/location/india-jobs/27595/1269750/2",
    "linkedin_search": "Intuit Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://jobs.intuit.com",
    "region": "global",
    "entry_lpa": "20–35",
    "notes": "TurboTax/QuickBooks maker. Bangalore office. Strong payer — 20+ LPA entry level.",
}

COMPANY_CONFIGS["Mastercard"] = {
    "type": "playwright",
    "careers_url": "https://careers.mastercard.com/us/en/search-results?keywords=software+engineer&location=India",
    "linkedin_search": "Mastercard Software Engineer India",
    "job_card_selector": "li.jobs-list-item",
    "title_selector": "a.job-title",
    "location_selector": "span.job-location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.mastercard.com",
    "region": "finance_tech",
    "entry_lpa": "15–25",
    "notes": "Gurgaon and Pune offices.",
}

COMPANY_CONFIGS["Rippling"] = {
    "type": "playwright",
    "careers_url": "https://www.rippling.com/careers?location=India",
    "linkedin_search": "Rippling Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.rippling.com",
    "region": "global",
    "entry_lpa": "25–40",
    "notes": "HR/payroll SaaS. Bangalore office. High payer — consistently 25+ LPA.",
}

COMPANY_CONFIGS["Workday"] = {
    "type": "playwright",
    "careers_url": "https://workday.wd5.myworkdayjobs.com/Workday?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
    "linkedin_search": "Workday Software Engineer India",
    "job_card_selector": "li.JLQJ4429",
    "title_selector": "a.css-19uc56f",
    "location_selector": "dd.css-129m7dg",
    "link_selector": "a.css-19uc56f",
    "apply_url_prefix": "https://workday.wd5.myworkdayjobs.com",
    "region": "global",
    "ats": "workday",
    "entry_lpa": "20–30",
    "notes": "HR/finance cloud software. Hyderabad and Pune offices.",
}

COMPANY_CONFIGS["Zendesk"] = {
    "type": "playwright",
    "careers_url": "https://jobs.zendesk.com/us/en/search-results?keywords=software+engineer&location=India",
    "linkedin_search": "Zendesk Software Engineer India",
    "job_card_selector": "li.jobs-list-item",
    "title_selector": "a.job-title",
    "location_selector": "span.job-location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://jobs.zendesk.com",
    "region": "global",
    "entry_lpa": "18–28",
    "notes": "Customer support SaaS. Bangalore office.",
}

COMPANY_CONFIGS["HubSpot"] = {
    "type": "playwright",
    "careers_url": "https://www.hubspot.com/careers/jobs?hubs_signup-cta=careers-all-dept&offset=0&department=Engineering&location=India",
    "linkedin_search": "HubSpot Software Engineer India",
    "job_card_selector": "li.opening",
    "title_selector": "a.opening-job-title",
    "location_selector": "span.location",
    "link_selector": "a.opening-job-title",
    "apply_url_prefix": "https://www.hubspot.com",
    "region": "global",
    "entry_lpa": "20–30",
    "notes": "CRM/marketing SaaS. Fully remote or Bangalore. 20+ LPA entry level.",
}

# ── Cybersecurity ─────────────────────────────────────────────────────────────

COMPANY_CONFIGS["Zscaler"] = {
    "type": "playwright",
    "careers_url": "https://www.zscaler.com/careers/search-jobs?location=India&keywords=software+engineer",
    "linkedin_search": "Zscaler Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.zscaler.com",
    "region": "global",
    "entry_lpa": "18–28",
    "notes": "Cloud security. Bangalore office.",
}

COMPANY_CONFIGS["SentinelOne"] = {
    "type": "playwright",
    "careers_url": "https://www.sentinelone.com/jobs/?location=India",
    "linkedin_search": "SentinelOne Software Engineer India",
    "job_card_selector": "div.job-item",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.sentinelone.com",
    "region": "global",
    "entry_lpa": "20–30",
    "notes": "AI cybersecurity. Bangalore office. Growing India presence.",
}

COMPANY_CONFIGS["Fortinet"] = {
    "type": "playwright",
    "careers_url": "https://www.fortinet.com/corporate/careers/search-jobs?location=India&keyword=software+engineer",
    "linkedin_search": "Fortinet Software Engineer India",
    "job_card_selector": "div.job-listing",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.fortinet.com",
    "region": "global",
    "entry_lpa": "15–25",
    "notes": "Network security. Bangalore office.",
}

COMPANY_CONFIGS["Wiz"] = {
    "type": "playwright",
    "careers_url": "https://www.wiz.io/company/careers?department=Engineering&location=India",
    "linkedin_search": "Wiz Software Engineer India",
    "job_card_selector": "li.opening",
    "title_selector": "a.opening-job-title",
    "location_selector": "span.location",
    "link_selector": "a.opening-job-title",
    "apply_url_prefix": "https://www.wiz.io",
    "region": "global",
    "entry_lpa": "25–40",
    "notes": "Cloud security unicorn. Remote India. High payer — backed by Google at $32B valuation.",
}

COMPANY_CONFIGS["Netskope"] = {
    "type": "playwright",
    "careers_url": "https://www.netskope.com/company/careers?location=India&department=Engineering",
    "linkedin_search": "Netskope Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.netskope.com",
    "region": "global",
    "entry_lpa": "18–28",
    "notes": "Cloud access security. Bangalore office.",
}

# ── Networking ────────────────────────────────────────────────────────────────

COMPANY_CONFIGS["Juniper Networks"] = {
    "type": "playwright",
    "careers_url": "https://jobs.juniper.net/search-jobs/software+engineer/India/829/1/2/6252001/39.26367/76.83617/100/1",
    "linkedin_search": "Juniper Networks Software Engineer India",
    "job_card_selector": "section.article--result",
    "title_selector": "h2 a",
    "location_selector": "span.job-location",
    "link_selector": "h2 a",
    "apply_url_prefix": "https://jobs.juniper.net",
    "region": "global",
    "entry_lpa": "12–22",
    "notes": "Networking hardware/software. Bangalore office. Consistent IIT recruiter.",
}

COMPANY_CONFIGS["Arista Networks"] = {
    "type": "playwright",
    "careers_url": "https://www.arista.com/en/careers/university/engineering?location=India",
    "linkedin_search": "Arista Networks Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.arista.com",
    "region": "global",
    "entry_lpa": "20–30",
    "notes": "Cloud networking. Bangalore office. 20+ LPA SDE-1.",
}

# ── Gaming / Entertainment ────────────────────────────────────────────────────

COMPANY_CONFIGS["Dream11"] = {
    "type": "playwright",
    "careers_url": "https://jobs.lever.co/dreamsports?team=Engineering",
    "linkedin_search": "Dream11 Software Engineer India",
    "job_card_selector": "div.posting",
    "title_selector": "h5 a",
    "location_selector": "span.location",
    "link_selector": "h5 a",
    "apply_url_prefix": "https://jobs.lever.co",
    "region": "indian_unicorn",
    "ats": "lever",
    "entry_lpa": "20–35",
    "notes": "World's largest fantasy sports platform. Mumbai HQ. 200M+ users. Strong tech team.",
}

COMPANY_CONFIGS["Games24x7"] = {
    "type": "requests",
    "careers_url": "https://www.games24x7.com/careers",
    "linkedin_search": "Games24x7 Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.games24x7.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "RummyCircle + My11Circle. Mumbai & Bangalore. IIT recruiter.",
}

COMPANY_CONFIGS["WinZO"] = {
    "type": "requests",
    "careers_url": "https://www.winzogames.com/careers",
    "linkedin_search": "WinZO Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.winzogames.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Gaming platform. Delhi HQ. Note: pivoting post India gaming regulation changes 2025.",
}

# ── Indian Fintech / Consumer Tech ───────────────────────────────────────────

COMPANY_CONFIGS["Upstox"] = {
    "type": "playwright",
    "careers_url": "https://upstox.com/careers/?department=Engineering",
    "linkedin_search": "Upstox Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://upstox.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Stock trading platform. Mumbai HQ. Backed by Tiger Global.",
}

COMPANY_CONFIGS["Angel One"] = {
    "type": "playwright",
    "careers_url": "https://www.angelone.in/careers?department=Technology",
    "linkedin_search": "Angel One Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.angelone.in",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Stock brokerage + fintech. Mumbai HQ.",
}

COMPANY_CONFIGS["INDMoney"] = {
    "type": "playwright",
    "careers_url": "https://www.indmoney.com/careers?department=Engineering",
    "linkedin_search": "INDMoney Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.indmoney.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–22",
    "notes": "Personal finance & US stocks app. Gurgaon HQ.",
}

COMPANY_CONFIGS["CoinDCX"] = {
    "type": "playwright",
    "careers_url": "https://coindcx.com/careers?department=Engineering",
    "linkedin_search": "CoinDCX Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://coindcx.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Crypto exchange. Mumbai HQ. India's largest crypto platform.",
}

COMPANY_CONFIGS["Tata 1mg"] = {
    "type": "playwright",
    "careers_url": "https://www.1mg.com/careers?department=Technology",
    "linkedin_search": "Tata 1mg Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.1mg.com",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Online pharmacy + health platform owned by Tata. Gurgaon HQ.",
}

COMPANY_CONFIGS["PharmEasy"] = {
    "type": "playwright",
    "careers_url": "https://pharmeasy.in/careers?department=Technology",
    "linkedin_search": "PharmEasy Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://pharmeasy.in",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Online pharmacy unicorn. Mumbai HQ.",
}

COMPANY_CONFIGS["ClearTax"] = {
    "type": "playwright",
    "careers_url": "https://cleartax.in/s/careers?department=Engineering",
    "linkedin_search": "ClearTax Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://cleartax.in",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Tax filing SaaS. Bangalore HQ.",
}

COMPANY_CONFIGS["IndiaMart"] = {
    "type": "playwright",
    "careers_url": "https://careers.indiamart.com/jobs?category=Technology",
    "linkedin_search": "IndiaMart Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.indiamart.com",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "B2B marketplace. Noida HQ. Listed company.",
}

COMPANY_CONFIGS["Ninjacart"] = {
    "type": "playwright",
    "careers_url": "https://ninjacart.in/careers?department=Engineering",
    "linkedin_search": "Ninjacart Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://ninjacart.in",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Agri supply chain. Bangalore HQ. Backed by Tiger Global and Walmart.",
}

COMPANY_CONFIGS["Lenskart"] = {
    "type": "playwright",
    "careers_url": "https://careers.lenskart.com/jobs?department=Technology",
    "linkedin_search": "Lenskart Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://careers.lenskart.com",
    "region": "indian_unicorn",
    "entry_lpa": "12–20",
    "notes": "Eyewear e-commerce unicorn. New Delhi / Gurgaon HQ.",
}

COMPANY_CONFIGS["Zepto"] = {
    "type": "playwright",
    "careers_url": "https://www.zeptonow.com/careers?department=Engineering",
    "linkedin_search": "Zepto Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.zeptonow.com",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Quick commerce. Mumbai HQ. Fast-growing unicorn, active IIT recruiter.",
}

# ── AI / Conversational AI ────────────────────────────────────────────────────

COMPANY_CONFIGS["Yellow AI"] = {
    "type": "playwright",
    "careers_url": "https://yellow.ai/careers/?department=Engineering",
    "linkedin_search": "Yellow AI Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://yellow.ai",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Conversational AI platform. Bangalore HQ. 1000+ enterprise customers.",
}

COMPANY_CONFIGS["Gupshup"] = {
    "type": "playwright",
    "careers_url": "https://www.gupshup.io/resources/careers?department=Engineering",
    "linkedin_search": "Gupshup Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.gupshup.io",
    "region": "indian_unicorn",
    "entry_lpa": "15–25",
    "notes": "Messaging API & conversational AI. San Francisco + Bangalore. Unicorn.",
}

COMPANY_CONFIGS["Eightfold AI"] = {
    "type": "playwright",
    "careers_url": "https://eightfold.ai/careers/?department=Engineering",
    "linkedin_search": "Eightfold AI Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://eightfold.ai",
    "region": "global",
    "entry_lpa": "20–30",
    "notes": "AI talent intelligence. Noida India office. Unicorn.",
}

COMPANY_CONFIGS["Leena AI"] = {
    "type": "playwright",
    "careers_url": "https://leena.ai/careers?department=Engineering",
    "linkedin_search": "Leena AI Software Engineer India",
    "job_card_selector": "div.job-card",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://leena.ai",
    "region": "indian_unicorn",
    "entry_lpa": "15–22",
    "notes": "Autonomous AI agents for enterprises. Gurgaon HQ.",
}

# ── Additional Quant / Finance ────────────────────────────────────────────────

COMPANY_CONFIGS["Jane Street"] = {
    "type": "requests",
    "careers_url": "https://www.janestreet.com/join-jane-street/open-roles/?type=campus-hire",
    "linkedin_search": "Jane Street Software Engineer India",
    "job_card_selector": "div.openings-job",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.janestreet.com",
    "region": "hft_quant",
    "entry_lpa": "80–150+",
    "notes": "Top HFT firm globally. No India office — but hires from IITs for global roles (Singapore/London/NY). Among the highest-paying employers for IIT grads.",
}

COMPANY_CONFIGS["Two Sigma"] = {
    "type": "playwright",
    "careers_url": "https://careers.twosigma.com/careers/SearchJobs?locationIdList=india",
    "linkedin_search": "Two Sigma Software Engineer India",
    "job_card_selector": "li.article--result",
    "title_selector": "h2 a",
    "location_selector": "span.job-location",
    "link_selector": "h2 a",
    "apply_url_prefix": "https://careers.twosigma.com",
    "region": "hft_quant",
    "entry_lpa": "50–100+",
    "notes": "Quant hedge fund. No India office — hires IIT grads for global roles. Entry SWE ~$247K USD.",
}

COMPANY_CONFIGS["Squarepoint Capital"] = {
    "type": "requests",
    "careers_url": "https://www.squarepointcap.com/careers",
    "linkedin_search": "Squarepoint Capital Software Engineer India",
    "job_card_selector": "div.job-listing",
    "title_selector": "a.job-title",
    "location_selector": "span.location",
    "link_selector": "a.job-title",
    "apply_url_prefix": "https://www.squarepointcap.com",
    "region": "hft_quant",
    "entry_lpa": "40–80",
    "notes": "Systematic quant fund. IIT campus recruiter. Gurgaon office.",
}


# =============================================================================
#  UPDATE HELPER GROUPINGS with new companies
# =============================================================================

# Add new companies to appropriate lists
_new_global = [
    "Cadence", "Synopsys", "KLA", "Ansys", "MathWorks", "Autodesk",
    "Western Digital", "NetApp", "Broadcom", "Commvault",
    "Intuit", "Mastercard", "Rippling", "Workday", "Zendesk", "HubSpot",
    "Zscaler", "SentinelOne", "Fortinet", "Wiz", "Netskope",
    "Juniper Networks", "Arista Networks",
    "Eightfold AI",
]
GLOBAL_TECH_COMPANIES.extend(_new_global)

_new_unicorns = [
    "Dream11", "Games24x7", "WinZO",
    "Upstox", "Angel One", "INDMoney", "CoinDCX",
    "Tata 1mg", "PharmEasy", "ClearTax", "IndiaMart",
    "Ninjacart", "Lenskart", "Zepto",
    "Yellow AI", "Gupshup", "Leena AI",
]
INDIAN_UNICORN_COMPANIES.extend(_new_unicorns)

_new_hft = ["Jane Street", "Two Sigma", "Squarepoint Capital"]
HFT_QUANT_COMPANIES.extend(_new_hft)

# Rebuild ALL_COMPANIES
ALL_COMPANIES = (
    INDIAN_IT_COMPANIES
    + GLOBAL_TECH_COMPANIES
    + HFT_QUANT_COMPANIES
    + INDIAN_UNICORN_COMPANIES
    + MNC_SERVICES_COMPANIES
    + FINANCE_TECH_COMPANIES
)

# Add high-pay new entries to HIGH_PAY_COMPANIES
_new_high_pay = [
    "Intuit", "Rippling", "Wiz", "Dream11", "Zepto",
    "Cadence", "Synopsys", "KLA", "MathWorks", "Autodesk", "NetApp",
    "Jane Street", "Two Sigma", "Squarepoint Capital",
    "HubSpot", "Workday", "SentinelOne", "Eightfold AI",
    "Arista Networks", "Mastercard", "Western Digital",
]
HIGH_PAY_COMPANIES.extend(_new_high_pay)