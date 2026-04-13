"""
source_google.py
Workaround scraper: uses Google search to find LinkedIn profiles
without ever logging into LinkedIn.

Query format: site:linkedin.com/in "<role>" "<location>"
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def _human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def _build_driver():
    """Create a Chrome driver with anti-detection settings."""
    options = Options()
    # Uncomment to hide the browser:
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # Persistent profile so Google trusts the browser
    options.add_argument(
        "--user-data-dir=/Users/rishitgambhir17/Library/Application Support/Google/Chrome-Selenium-Google"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def _build_query(role, location):
    """Build a Google dork query for LinkedIn profiles."""
    return f'site:linkedin.com/in "{role}" "{location}"'


def _do_search(driver, query):
    """Open Google and run the search query."""
    encoded = query.replace(' ', '+').replace('"', '%22')
    url = f"https://www.google.com/search?q={encoded}"
    driver.get(url)
    _human_delay(2, 4)
    print(f"DEBUG: Google search URL → {url}")


def _extract_results(driver, count):
    """Pull the top N LinkedIn results from the Google results page."""
    candidates = []

    # Wait up to 10s for search results to render
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#search"))
        )
    except Exception:
        print("DEBUG: Google results never rendered")
        return candidates

    # Each result is in a div with class 'g' (Google's standard results container)
    # We extract the title (name + headline), URL, and snippet
    js_query = """
    const results = [];
    document.querySelectorAll('a').forEach(a => {
        const href = a.href || '';
        if (!href.includes('linkedin.com/in/')) return;
        // Find the heading (h3) inside this anchor — Google's standard result title
        const h3 = a.querySelector('h3');
        if (!h3) return;
        const title = h3.innerText || '';
        // Walk up to the result container and get the snippet text
        let container = a.closest('div.g') || a.closest('[data-sokoban-container]') || a.parentElement.parentElement;
        let snippet = '';
        if (container) {
            const snippetEl = container.querySelector('div[data-sncf], div.VwiC3b, span.aCOpRe');
            if (snippetEl) snippet = snippetEl.innerText || '';
        }
        results.push({ title, href: href.split('?')[0], snippet });
    });
    return results;
    """

    try:
        raw = driver.execute_script(js_query)
    except Exception as e:
        print(f"DEBUG: JS extraction failed: {e}")
        return candidates

    print(f"DEBUG: JS returned {len(raw)} LinkedIn results from Google")

    seen = set()
    for item in raw:
        href = item.get("href", "")
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "").strip()
        if href in seen or not title:
            continue
        seen.add(href)

        # Google titles for LinkedIn pages look like:  "Aman Sharma - Senior Python Developer at Flipkart - LinkedIn"
        # Split on " - " and take the first part as the name
        parts = title.split(" - ")
        name = parts[0].strip() if parts else title
        headline = parts[1].strip() if len(parts) > 1 else "N/A"

        candidates.append({
            "name": name,
            "role": headline,
            "experience": "N/A",
            "location": "From snippet",
            "profile_url": href,
            "snippet": snippet[:200],
        })
        if len(candidates) >= count:
            break

    return candidates


def run(role="Software Engineer", location="India", count=3):
    """
    Main entry point called by search.py router.
    Uses Google search to find public LinkedIn profiles.
    """
    driver = None
    try:
        driver = _build_driver()
        query = _build_query(role, location)
        print(f"DEBUG: Google query → {query}")
        _do_search(driver, query)

        # Save debug screenshot + HTML
        driver.save_screenshot("/tmp/google_debug.png")
        with open("/tmp/google_debug.html", "w") as f:
            f.write(driver.page_source)
        print("DEBUG: saved /tmp/google_debug.png and /tmp/google_debug.html")

        candidates = _extract_results(driver, count)
        return candidates if candidates else [{"error": "No candidates found via Google"}]
    except Exception as e:
        return [{"error": f"Google scraper failed: {str(e)}"}]
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    results = run(role="C++ Developer", location="Delhi", count=3)
    for r in results:
        print(r)