# AI Recruitment Bot

A Telegram bot that takes plain-English hiring requests and returns real candidate profiles from LinkedIn.

Built during my AI Engineering internship at VVDN Technologies.

## The idea

A hiring manager opens Telegram and types:

    I need 3 Python developers in Bangalore

The bot parses that, runs a search, and replies with a short list of real profiles — names, headlines, LinkedIn URLs.

No form to fill. No dashboard to log into. Just chat.

## How it works

The flow is:

    Telegram  →  OpenClaw  →  LLM  →  linkedin_search skill  →  source module  →  results

- **OpenClaw** runs the agent loop, talks to Telegram, and invokes skills. Think of it as the backbone.
- **LLM** is gpt-oss-120b (via OpenRouter, free tier). It decides when to call the skill and with what arguments.
- **linkedin_search** is the skill we built. It has one job: given a role + location + count, return candidates.
- **Source modules** sit inside the skill. The skill delegates to whichever source is selected in the config. This is the important design decision — see below.

## Why pluggable sources matter

The first version of this project tried to scrape LinkedIn directly with Selenium. That turned into a rabbit hole (detailed in docs/SELENIUM_ATTEMPT.md). The short version: LinkedIn's anti-bot architecture in 2026 makes direct scraping very hard, and weak accounts return "LinkedIn Member" instead of real names.

So instead of fighting that war, I designed the skill around a **swappable source** pattern. The skill exposes one function. Behind it, any of these can fetch the data:

| Source | File | What it does | Status |
|---|---|---|---|
| google | sources/source_google.py | Google search for public LinkedIn pages, parses titles and snippets | **Working, current default** |
| mock | sources/source_mock.py | Returns 5 hardcoded fake candidates | Fallback for offline testing |
| selenium | sources/source_selenium.py | Direct LinkedIn scraper with login, anti-detection, JS injection | Documented attempt. Blocked by LinkedIn. |

Switching between them is a single env var change: SOURCE_TYPE=google|mock|selenium. The router in search.py picks the right one.

## Extending with other data sources

The Google-search approach works well for a demo but has real limits: Google will eventually throttle automated queries, and the data per candidate is limited to whatever appears in the search snippet (name, headline, URL — no skills, experience, company history).

If richer data is needed later — full skills, past companies, years of experience, education — the skill is architected so any new data source can be plugged in without rewriting the rest of the bot.

The steps to add a new source would be:

1. Drop a new file at sources/source_<name>.py that exposes a run(role, location, count) function and returns the same shape of dict as the other sources.
2. Add any required credentials to .env.
3. Add an elif branch in search.py to route SOURCE_TYPE=<name> to the new module.

That's it. No changes to the bot, the OpenClaw integration, SKILL.md, or anything else. The scraping strategy is an implementation detail, not a dependency of the rest of the system.

## Setup

### What you need first
- Python 3.11+
- Google Chrome installed
- OpenClaw CLI: npm install -g openclaw
- A Telegram bot token (get one from @BotFather on Telegram)
- An OpenRouter API key (sign up at openrouter.ai, free tier is fine)

### Clone and install
    git clone https://github.com/rishit1702/ai_recruitment_bot.git
    cd ai_recruitment_bot
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Fill in .env
    cp .env.example .env

Then open .env and set SOURCE_TYPE=google. The LinkedIn email/password fields are only needed if you set SOURCE_TYPE=selenium (not recommended).

### Register the skill with OpenClaw
OpenClaw loads skills from ~/.openclaw/workspace/skills/. Copy the skill folder in:

    cp -R skills/linkedin_search ~/.openclaw/workspace/skills/
    cp .env ~/.openclaw/workspace/skills/linkedin_search/.env

Verify OpenClaw sees it:

    openclaw skills info linkedin_search

Should show "Ready". If not, check SKILL.md has valid YAML frontmatter.

### Run it
    openclaw gateway --force

Then message your Telegram bot. Try: "find me 3 C++ developers in Delhi".

## Testing the skill on its own (without OpenClaw)
    cd skills/linkedin_search
    python search.py

This runs the skill directly with a hardcoded test query and prints results to stdout. Useful when you're iterating on a source module.

## Design notes

- **Secrets never in git.** .env is gitignored. .env.example is the template with empty values. Anyone cloning the repo has to fill in their own.
- **Skill format follows AgentSkills spec.** SKILL.md starts with YAML frontmatter (name + description) — OpenClaw parses this to decide when to invoke the skill. Without valid frontmatter, OpenClaw silently ignores the skill (learned this the hard way).
- **Router lives in search.py.** Single entry point for the skill. All branching on SOURCE_TYPE happens here. Keeps source modules simple and unaware of each other.

## Author
Rishit Gambhir  
AI Engineering Intern, VVDN Technologies  
