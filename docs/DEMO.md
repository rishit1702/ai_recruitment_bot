# Demo Guide

Quick walkthrough for running the bot end-to-end.

## Prerequisites (one-time setup)

1. Clone the repo and install Python dependencies (see main README).
2. Install OpenClaw: `npm install -g openclaw`
3. Create a Telegram bot via @BotFather, save the token.
4. Create an OpenRouter account (free tier), save the API key.
5. Run `openclaw onboard` and paste both tokens when prompted.
6. Copy the skill into the OpenClaw workspace:

       cp -R skills/linkedin_search ~/.openclaw/workspace/skills/
       cp .env ~/.openclaw/workspace/skills/linkedin_search/.env

7. Verify: `openclaw skills info linkedin_search` should show "Ready".

## Running the demo

In one terminal, start the gateway:

    openclaw gateway --force

Watch the logs — you should see:
- `[gateway] agent model: openrouter/openai/gpt-oss-120b:free`
- `[telegram] [default] starting provider (@YourBotName)`

Leave this terminal running.

## Testing from Telegram

Open Telegram, find your bot, send:

    need 3 Python developers in Bangalore

Expected reply (takes 5-10 seconds):

    Found 3 candidates for Python Developer in Bangalore:

    1. Mithlesh Kumar — Python, Django Developer
       https://in.linkedin.com/in/mithlesh-kumar-28907823

    2. Priyanshu Bajpai — Python Developer | Data Science & ML
       https://in.linkedin.com/in/priyanshu-bajpai-6069b2384

    3. Shreeya Naganur — Python developer at TCS, Bangalore
       https://in.linkedin.com/in/shreeyanaganur

## Other queries to try

- "Find me 5 C++ engineers in Delhi"
- "Hiring frontend devs in Mumbai"
- "Show me 3 data scientists"
- "Need backend Java people in Pune"

## Testing the skill without OpenClaw

To test just the data fetch layer:

    cd skills/linkedin_search
    source ../../venv/bin/activate
    python search.py

This runs a hardcoded query and prints results to stdout. Switch sources by editing SOURCE_TYPE in .env:

- SOURCE_TYPE=google  — live Google search (default)
- SOURCE_TYPE=mock    — returns fake candidates, useful when offline

## Troubleshooting

**Bot replies but asks clarifying questions instead of searching.**  
SKILL.md is not loaded. Run `openclaw skills info linkedin_search` — should show "Ready". If not, check the YAML frontmatter in SKILL.md.

**Bot does not reply at all.**  
Check the OpenClaw gateway terminal for errors. Most common: OpenRouter key is invalid or rate-limited.

**Selenium source returns empty.**  
Expected. Selenium is the documented-failed approach (see SELENIUM_ATTEMPT.md). Use SOURCE_TYPE=google.

**Google source returns empty.**  
Google may be showing a CAPTCHA. Run the skill standalone (see above), watch the Chrome window, solve the CAPTCHA once manually. The persistent profile will remember it.
