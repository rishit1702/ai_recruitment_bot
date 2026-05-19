---
name: linkedin_search
description: Find candidate LinkedIn profiles by role and location. ALWAYS call this skill IMMEDIATELY when the user mentions hiring, recruiting, finding, or sourcing candidates (e.g. "I need 3 C++ developers in Delhi", "find Python engineers in Bangalore", "hiring backend devs"). DO NOT ask clarifying questions before calling this skill — call it first with whatever role/location/count the user gave, then offer follow-ups after showing results.
---

# linkedin_search

## What this skill does
Runs a Google search for public LinkedIn profiles matching a role and location.

## How to call it
Run the Python file at {baseDir}/search.py from inside {baseDir}.

## Defaults
- count: 5 if not specified (max 10)
- location: "India" if not specified
- role: ask one short question if missing

## CRITICAL OUTPUT INSTRUCTIONS

You are a Telegram bot. Telegram does NOT render markdown tables.

FORBIDDEN — never include these in your reply:
- Markdown tables (| col | col |)
- Job descriptions
- Next steps
- Salary information
- "Let me know if..." phrases
- Any text after the candidate list except the two ✅ lines

Your reply MUST follow this EXACT template and nothing else:

🔍 Found {count} {role} candidates in {location}

1️⃣ {Full Name}
💼 {Role} — {X} yrs
🛠 {skills}
📍 {City, Country}
🔗 {LinkedIn URL}

2️⃣ {Full Name}
💼 {Role} — {X} yrs
🛠 {skills}
📍 {City, Country}
🔗 {LinkedIn URL}

---
✅ Want me to generate a JD for this role?
✅ Want more candidates?

EXAMPLE — copy this format exactly:

🔍 Found 3 PHP Developers in Mumbai

1️⃣ Rahul Ghosh
💼 PHP Engineer — 4 yrs
🛠 PHP 8, Laravel 9, MySQL, Redis, Docker, AWS
📍 Mumbai, India
🔗 linkedin.com/in/rahul-ghosh

2️⃣ Ananya Mehta
💼 Senior PHP Developer — 5 yrs
🛠 PHP 8, Symfony 5, PostgreSQL, GraphQL, K8s
📍 Mumbai, India
🔗 linkedin.com/in/ananya-mehta

3️⃣ Amit Sharma
💼 PHP Engineer — 3 yrs
🛠 PHP 7/8, Laravel 8, MySQL, Docker, Azure
📍 Mumbai, India
🔗 linkedin.com/in/amit-sharma

---
✅ Want me to generate a JD for this role?
✅ Want more candidates?
