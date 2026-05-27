# AI Recruitment Bot

An end-to-end AI-powered recruitment pipeline built on Telegram. A hiring manager sends a plain-English message and the bot finds candidates, generates a Job Description, posts the job live on Internshala, fetches applicants, and returns a ranked shortlist — all from a single chat window.

Built during my AI Engineering internship at VVDN Technologies.

---

## What it does

| Step | Manager action | What happens |
|---|---|---|
| 1 | "Find 3 PHP devs Mumbai 5 YOE" | Bot scrapes Google for real LinkedIn profiles and returns a candidate list |
| 2 | "Generate JD" | Bot calls LLM API and returns a full formatted Job Description |
| 3 | Run 2 terminal commands | JD is parsed and posted live on Internshala via Chrome automation |
| 4 | Run 1 terminal command | Bot fetches applicants from Internshala dashboard |
| 5 | Run 1 terminal command | Bot ranks candidates by JD match and sends results to Telegram |

---

## Architecture

```
Manager types in Telegram
        ↓
OpenClaw (agent framework) → LLM (OpenRouter)
        ↓
Skills: linkedin_search / jd_generator
        ↓
Terminal: parse_jd.py → post_job_final.py → Internshala (Chrome)
        ↓
Terminal: fetch_applicants.py → rank.py → Telegram
```

---

## Project Structure

```
ai_recruitment_bot/
├── skills/
│   ├── linkedin_search/
│   │   ├── SKILL.md              # OpenClaw skill definition
│   │   ├── search.py             # Router — picks source module
│   │   └── sources/
│   │       ├── source_google.py  # Google scraper (default)
│   │       ├── source_mock.py    # Hardcoded test data
│   │       └── source_selenium.py # Direct LinkedIn (blocked)
│   └── jd_generator/
│       ├── SKILL.md              # OpenClaw skill definition
│       └── generate.py           # Calls LLM API, saves /tmp/last_jd.json
├── parse_jd.py                   # Parses JD text → /tmp/last_jd.json
├── post_job_final.py             # Selenium form filler for Internshala
├── fetch_applicants.py           # Scrapes applicants from Internshala dashboard
├── rank.py                       # Ranks candidates via LLM, sends to Telegram
├── applicants.json               # Mock applicant data for testing
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.11+
- Google Chrome installed
- Node.js 18+
- OpenClaw CLI: `npm install -g openclaw`
- A Telegram bot token
- An OpenRouter API key (free tier works)

### 1. Clone and install

```bash
git clone https://github.com/rishit1702/ai_recruitment_bot.git
cd ai_recruitment_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up OpenRouter

1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up and go to **Keys → Create Key**
3. Copy your API key

### 3. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Choose a name (e.g. `VVDN Recruiter`) and a username (e.g. `@VVDN_Recruiter_Bot`)
4. BotFather gives you a **bot token** — copy it
5. Get your **chat ID**:
   - Start a conversation with your bot
   - Open this URL in browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Send any message to the bot, refresh the URL
   - Find `"chat":{"id":XXXXXXXXX}` — that number is your chat ID

### 4. Configure OpenClaw

Create the OpenClaw config at `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "your_token_here"
    }
  },
  "agents": {
    "defaults": {
      "workspace": "/path/to/your/.openclaw/workspace",
      "models": {
        "meta-llama/llama-3.3-70b-instruct:free": {}
      },
      "timeoutSeconds": 600
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "dmPolicy": "allowlist",
      "allowFrom": [
        "YOUR_CHAT_ID"
      ]
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "openrouter": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "api": "openai-completions",
        "apiKey": "YOUR_OPENROUTER_API_KEY",
        "models": [
          {
            "id": "meta-llama/llama-3.3-70b-instruct:free",
            "name": "meta-llama/llama-3.3-70b-instruct:free",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0 }
          }
        ]
      }
    }
  },
  "plugins": {
    "entries": {
      "openrouter": { "enabled": true }
    }
  }
}
```

Replace:
- `YOUR_TELEGRAM_BOT_TOKEN` → token from BotFather
- `YOUR_CHAT_ID` → your Telegram chat ID
- `YOUR_OPENROUTER_API_KEY` → your OpenRouter key

### 5. Register skills with OpenClaw

```bash
cp -R skills/linkedin_search ~/.openclaw/workspace/skills/
cp -R skills/jd_generator ~/.openclaw/workspace/skills/
```

### 6. Set up Internshala Chrome session

Copy your logged-in Chrome profile so the bot can post jobs without re-login:

```bash
cp -r ~/Library/Application\ Support/Google/Chrome/Default /tmp/chrome_internshala_profile
```

If the session expires later, refresh it with:

```bash
rm -rf /tmp/chrome_internshala_profile && cp -r ~/Library/Application\ Support/Google/Chrome/Default /tmp/chrome_internshala_profile
```

### 7. Update bot token and chat ID in rank.py

Open `rank.py` and find these two lines near the bottom of the file (inside the `try` block after saving `/tmp/ranked_applicants.json`):

```python
tg_url = f"https://api.telegram.org/bot8670308700:AAG3WCi5led6l1J6XLOnIdM5VrZ4BINA_-E/sendMessage"
...
"chat_id": "943955595",
```

Replace with your own values:

```python
tg_url = f"https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage"
...
"chat_id": "YOUR_CHAT_ID",
```

Or run this one-liner to replace both at once (fill in your values first):

```bash
python3 -c "
content = open('rank.py').read()
content = content.replace('YOUR_OLD_BOT_TOKEN', 'YOUR_NEW_BOT_TOKEN')
content = content.replace('YOUR_OLD_CHAT_ID', 'YOUR_NEW_CHAT_ID')
open('rank.py','w').write(content)
print('done')
"
```

After this, running `rank.py` will automatically send the ranked list to your Telegram chat.

---

## Running the bot

### Start the bot

```bash
openclaw gateway
```

The bot is now live on Telegram.

### Post a job (after bot generates JD)

Copy the JD text from Telegram, then run:

```bash
cat > /tmp/last_jd_raw.txt
# Paste JD text here, then press Ctrl+D
```

```bash
/opt/homebrew/bin/python3 /tmp/parse_jd.py && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /opt/homebrew/bin/python3 /tmp/post_job_final.py
```

Chrome opens, fills the entire Internshala form, and clicks Post Job automatically.

### Fetch and rank applicants (after job goes live)

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /opt/homebrew/bin/python3 /tmp/fetch_applicants.py
/opt/homebrew/bin/python3 /tmp/rank.py
```

Ranked results are sent directly to your Telegram.

---

## Key Technical Notes

| Problem | Solution |
|---|---|
| LinkedIn blocks scraping | Google search fallback for public LinkedIn pages |
| Internshala salary fields reject send_keys | `nativeInputValueSetter` JS trick |
| Internshala description field rejects send_keys | `HTMLTextAreaElement` JS trick |
| OpenClaw can't run Python scripts | Scripts triggered manually from terminal |
| Chrome session auth | Copied from Default profile to `/tmp/chrome_internshala_profile` |
| Unicode chars in JD break form | Cleaned before passing to Selenium |

---

## Pluggable Source Architecture

The candidate search is designed around swappable source modules. Switch sources by setting `SOURCE_TYPE` in `.env`:

| Source | File | Status |
|---|---|---|
| `google` | `source_google.py` | Working — default |
| `mock` | `source_mock.py` | Offline testing |
| `selenium` | `source_selenium.py` | Blocked by LinkedIn |

Adding a new source: drop a file at `sources/source_<name>.py` exposing `run(role, location, count)` and add an `elif` branch in `search.py`. Nothing else changes.

---

## Environment

- macOS, M-series chip
- Python 3.14 (Homebrew) — always prefix with `DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib`
- Chrome 148
- OpenClaw 2026.4.5
- OpenRouter free tier (rate limit: ~20 req/min — use `/reset` in Telegram if context overflow occurs)

---

## Author

Rishit Gambhir  
AI Engineering Intern, VVDN Technologies  
[github.com/rishit1702](https://github.com/rishit1702)
