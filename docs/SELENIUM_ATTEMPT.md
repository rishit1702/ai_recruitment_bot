# Selenium LinkedIn Scraper — Attempt Log

This document describes the first approach I took for the candidate search part of the bot: scraping LinkedIn directly with Selenium. It does not work in production, but the code is committed because it represents several days of real engineering effort and the lessons are worth keeping.

The working approach (Google-search-based) lives in `sources/source_google.py` and is described in the main README.

## The plan

Use Selenium to drive a real Chrome browser:

1. Log into LinkedIn with a throwaway account.
2. Navigate to the People search URL for a given role and location.
3. Extract the top N profiles — name, headline, profile URL.
4. Return them in the same dict shape as the other source modules.

Standard scraping pattern. On paper, straightforward.

## What I built

`sources/source_selenium.py` implements the full flow with several production-grade details:

- **Anti-detection Chrome flags**
  - Custom user-agent string (mimics real macOS Chrome)
  - `--disable-blink-features=AutomationControlled` to hide the webdriver flag
  - `excludeSwitches` and `useAutomationExtension` to remove Selenium's fingerprints
  - `navigator.webdriver` overridden via `execute_script` to return `undefined`
- **Persistent Chrome profile** at `~/Library/Application Support/Google/Chrome-Selenium-LinkedIn` so LinkedIn cookies and "trusted device" status survive between runs.
- **Random human-like delays** between every action (2-6 seconds, uniform random) to avoid pattern-based detection.
- **Login flow** that first tries `/feed/` — if the persistent profile still has a valid session, it skips the login page entirely.
- **Lazy-load handling** — after navigating to the search URL, the script waits 8 seconds, scrolls incrementally (400px, 800px, 1200px), scrolls back to top, then waits up to 15 more seconds for profile links to appear.
- **JavaScript injection for extraction** — instead of Selenium's CSS selectors, which can't pierce shadow DOMs, the script uses `driver.execute_script()` to run JS from inside the page. The JS walks the DOM and returns all `<a>` tags with `linkedin.com/in/` hrefs.
- **Debug artifacts** — every run saves a screenshot to `/tmp/linkedin_debug.png` and the page HTML to `/tmp/linkedin_debug.html` so failures can be inspected after the fact.
- **Always cleans up** via `try/finally` — `driver.quit()` always runs so orphan Chrome processes don't accumulate.

## What broke it

Three blockers, in order of discovery. None of them are code bugs — they are structural.

### Blocker 1: Results render inside closed shadow DOMs

LinkedIn's search results page uses custom web components. The actual candidate cards live inside closed shadow DOMs attached to these components.

- `driver.page_source` returns the outer HTML only — everything inside a shadow DOM is invisible to it.
- `driver.find_elements(By.CSS_SELECTOR, ...)` also cannot cross shadow-DOM boundaries by default.
- `driver.execute_script()` running JS in the page context *can* sometimes reach into shadow DOMs, but LinkedIn's are **closed** shadow roots, which deny programmatic access even from same-page JS.

Result: the browser visibly shows candidate cards on screen for 20+ seconds, but every programmatic query — Selenium, page_source, injected JS — returns zero profile links.

### Blocker 2: LinkedIn Member anonymization

Even if the shadow-DOM problem were solved, the scraper would return unusable data. LinkedIn shows profiles as "LinkedIn Member" — not the real name — to viewers whose account is:

- Less than a few weeks old
- Has fewer than ~50 connections
- Outside the 2nd/3rd-degree network of the profile being viewed

This applied to the throwaway account I used. Aging the account and building a real connection network would take 2-3 weeks minimum and still might not fully resolve it.

### Blocker 3: Free-tier search quota

LinkedIn limits free accounts to roughly 5-10 People searches per month before showing a "You've reached the monthly limit — upgrade to Premium" banner. Hit during testing.

## Why I kept the code

- It demonstrates real Selenium engineering: persistent profiles, anti-detection, explicit waits, JS injection, cleanup discipline.
- It documents a real engineering decision with evidence — "scraping LinkedIn directly is not viable in 2026 without a Premium account" is a claim that's easier to believe when backed by a working, failing script and three specific blockers.
- It's a clean fallback implementation if LinkedIn ever loosens its restrictions or if someone wants to run it with a Premium Sales Navigator account in the future.

## What I did instead

Pivoted to Google search of public LinkedIn pages. Google renders its results as plain server-rendered HTML, shows real names (LinkedIn's SEO-facing version is not anonymized), and doesn't require an account.

See `sources/source_google.py` for the working implementation and the main README for how it slots into the pluggable-source architecture.
