"""
The candidate profile every scraped job is scored against.

Edit this to match your real background — the LLM enrichment step in llm/enrich.py
puts this profile directly in the prompt, so the more specific it is, the sharper
the match_score and pitch it produces. This is deliberately a plain dict (not a
database row) so you can tune it without touching code elsewhere.
"""

USER_PROFILE = {
    "experience_years": 1,
    "target_titles": [
        "Software Engineer",
        "Backend Engineer",
        "Full Stack Developer",
        "Mobile Engineer",
        "SDE",
        "Associate Software Engineer",
    ],
    "core_skills": [
        "Python",
        "TypeScript",
        "JavaScript",
        "React",
        "React Native",
        "Node.js",
        "SQL",
        "REST APIs",
        "Git",
    ],
    "interested_in": [
        "backend systems",
        "developer tools",
        "mobile apps",
        "early-stage product work",
    ],
    "location_pref": "India — Bangalore, Hyderabad, Pune, remote-India",
    "summary": (
        "Early-career software engineer (0-2 yrs), comfortable across the stack. "
        "Recently shipped a full React Native app end-to-end — design system, game "
        "logic, state management, and a CI/EAS build pipeline — and built a "
        "multi-threaded Python job scraper across 150+ companies with ATS-aware "
        "scrapers (Greenhouse/Lever/Workday APIs) and a rule-based filter pipeline. "
        "Looking for roles with real ownership over a product surface, not pure "
        "maintenance work."
    ),
}
