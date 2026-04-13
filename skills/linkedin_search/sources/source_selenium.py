"""
source_selenium.py
Real LinkedIn scraper using Selenium + Chrome.
Called by search.py router when SOURCE_TYPE=selenium.
"""

import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load credentials from .env
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")


def _human_delay(min_sec=2, max_sec=5):
    """Sleep a random amount to look less bot-like."""
    time.sleep(random.uniform(min_sec, max_sec))


def _build_driver():
    """Create a Chrome driver with anti-detection settings."""
    options = Options()
    # Comment the next line if you want to WATCH the browser (useful for debugging)
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def _login(driver):
    """Log into LinkedIn. Skips if already logged in via persistent profile."""
    driver.get("https://www.linkedin.com/feed/")
    _human_delay(3, 5)

    if "feed" in driver.current_url and "login" not in driver.current_url:
        print("✅ Already logged in via persistent profile.")
        return

    driver.get("https://www.linkedin.com/login")
    _human_delay(2, 4)

    email_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_box.send_keys(LINKEDIN_EMAIL)
    _human_delay(1, 2)

    pw_box = driver.find_element(By.ID, "password")
    pw_box.send_keys(LINKEDIN_PASSWORD)
    _human_delay(1, 2)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    _human_delay(5, 8)
    print("✅ Login submitted, continuing...")



def _search_people(driver, role, location):
    """Run LinkedIn People search and wait for results to render."""
    query = f"{role} {location}".replace(" ", "%20")
    url = f"https://www.linkedin.com/search/results/people/?keywords={query}"
    driver.get(url)
    print(f"DEBUG: navigated to {url}")

    # Give React 8 seconds minimum to mount
    time.sleep(8)

    # Scroll slowly to trigger lazy rendering
    for i in range(3):
        driver.execute_script(f"window.scrollTo(0, {(i+1) * 400});")
        time.sleep(2)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # Wait up to 15s more for profile links to appear
    try:
        WebDriverWait(driver, 15).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")) > 0
        )
        print("DEBUG: profile links detected in DOM ✓")
    except Exception:
        print("DEBUG: no profile links found after wait ✗")

def _extract_candidates(driver, count):
    import time
    
    # scroll to load profiles
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    js_query = """
    return Array.from(document.querySelectorAll("a"))
        .map(a => ({
            href: a.href,
            text: a.innerText || a.textContent || ""
        }))
        .filter(item => 
            item.href && 
            item.href.includes('/in/') && 
            !item.href.includes('/in/me')
        );
    """

    results = driver.execute_script(js_query)
    return results[:count]

    try:
        raw = driver.execute_script(js_query)
    except Exception as e:
        print(f"DEBUG: JS execution failed: {e}")
        return candidates

    print(f"DEBUG: JS returned {len(raw)} raw profile links")

    seen = set()
    for item in raw:
        href = item.get("href", "").split("?")[0]
        text = item.get("text", "").strip()
        if href in seen or not text:
            continue
        seen.add(href)
        candidates.append({
            "name": text.split("\n")[0][:100],
            "role": "N/A",
            "experience": "N/A",
            "location": "N/A",
            "profile_url": href,
        })
        if len(candidates) >= count:
            break

    return candidates


def run(role="Software Engineer", location="India", count=3):
    """
    Main entry point called by search.py router.
    Returns a list of candidate dicts in the same shape as source_mock.
    """
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        return [{"error": "LinkedIn credentials missing in .env"}]

    driver = None
    try:
        driver = _build_driver()
        _login(driver)
        _search_people(driver, role, location)

        # DEBUG: screenshot so we can visually verify what Selenium sees
        driver.save_screenshot("/tmp/linkedin_debug.png")
        print("DEBUG: screenshot saved to /tmp/linkedin_debug.png")

        # DEBUG: count profile links via Selenium directly (not page_source)
        profile_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")
        print(f"DEBUG: Selenium found {len(profile_links)} profile links in DOM")

        # DEBUG: dump page HTML too for inspection
        with open("/tmp/linkedin_debug.html", "w") as f:
            f.write(driver.page_source)
        print(f"DEBUG: current URL: {driver.current_url}")

        # DEBUG: print first 5 profile URLs if found
        for i, link in enumerate(profile_links[:5]):
            try:
                href = link.get_attribute("href")
                text = link.text.strip()[:50]
                print(f"  link {i+1}: {href} | text='{text}'")
            except Exception:
                pass

    

        candidates = _extract_candidates(driver, count)
        return candidates if candidates else [{"error": "No candidates found"}]
    except Exception as e:
        return [{"error": f"Scraper failed: {str(e)}"}]
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Quick test: run directly with python source_selenium.py
    results = run(role="Python Developer", location="Bangalore", count=3)
    for r in results:
        print(r)