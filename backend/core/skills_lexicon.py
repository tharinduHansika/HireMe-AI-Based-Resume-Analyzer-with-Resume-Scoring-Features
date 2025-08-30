# backend/core/skills_lexicon.py
# Lightweight lexicon + helpers (no external deps)

# Single-word skills (lowercase)
SKILL_WORDS = {
    # programming
    "python", "java", "javascript", "typescript", "html", "css", "sql", "mysql", "postgres", "git",
    "react", "next.js", "nextjs", "node", "node.js", "nodejs", "jquery", "jira",
    "wordpress", "tailwind", "bootstrap", "selenium",
    # data / analytics
    "excel", "tableau", "powerbi", "power-bi", "bigquery", "ga4", "ga", "analytics", "bi",
    # product / web
    "ux", "ui", "rest", "api", "apis", "seo", "sem",
    # process
    "agile", "scrum", "kanban",
    # design / media
    "photoshop", "illustrator", "after-effects", "premiere", "indesign",
    # social / marketing
    "facebook", "instagram", "tiktok",
}

# Multi-word phrases (lowercase); keep short, unambiguous phrases
SKILL_PHRASES = {
    "html/css", "html / css", "front-end", "front end", "back-end", "back end",
    "google analytics", "google analytics 4", "power bi", "data analysis",
    "data visualization", "content marketing", "social media", "unit testing",
    "continuous integration", "rest api", "rest apis",
}

# Canonicalization map -> pretty labels
CANONICAL = {
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "ga4": "Google Analytics 4",
    "ga": "Google Analytics",
    "powerbi": "Power BI",
    "power-bi": "Power BI",
    "html": "HTML",
    "css": "CSS",
    "sql": "SQL",
    "ux": "UX",
    "ui": "UI",
}

# Words we never want to show as skills
BANNED_TOKENS = {
    "associate", "currently", "present", "hons", "summary", "professional",
    "year", "years", "month", "months", "gmail.com", "linkedin", "www", "com",
    "sri", "lanka", "metropolitan", "university", "cardiff", "engineer", "developer",
    "manager", "company", "project", "projects", "design", "product", "system"
}
