import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import urllib.request

# ── Chrome setup with saved session ─────────────────────────────────────────
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/tmp/chrome_internshala_profile")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# ── Go to applications page ──────────────────────────────────────────────────
driver.get("https://internshala.com/employer/dashboard")
time.sleep(4)

# Click Jobs tab
try:
    jobs_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Jobs')] | //li[contains(text(),'Jobs')]")
    driver.execute_script("arguments[0].click();", jobs_tab)
    time.sleep(2)
except:
    pass

# Click on first job listing
try:
    job_row = driver.find_element(By.CSS_SELECTOR, "table tr td a, .job-title a, td.job-title")
    driver.execute_script("arguments[0].click();", job_row)
    time.sleep(3)
except Exception as e:
    print("Could not click job row:", e)

# Take screenshot to see applicant page structure
driver.save_screenshot("/tmp/applicants_page.png")
print("Screenshot saved to /tmp/applicants_page.png")

# Try scraping applicant cards
applicants = []
try:
    cards = driver.find_elements(By.CSS_SELECTOR, ".applicant-card, .application-card, .candidate-card, tr.applicant")
    print(f"Found {len(cards)} applicant cards")
    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, ".name, .applicant-name, h3, h4").text.strip()
        except:
            name = "Unknown"
        try:
            exp = card.find_element(By.CSS_SELECTOR, ".experience, .exp").text.strip()
        except:
            exp = ""
        try:
            skills = card.find_element(By.CSS_SELECTOR, ".skills, .skill-tags").text.strip()
        except:
            skills = ""
        applicants.append({"name": name, "experience": exp, "skills": skills})
        print(f"  - {name} | {exp} | {skills}")
except Exception as e:
    print("Scraping error:", e)

if applicants:
    with open("/tmp/applicants.json", "w") as f:
        json.dump(applicants, f, indent=2)
    print(f"\nSaved {len(applicants)} applicants to /tmp/applicants.json")
else:
    print("No applicants found yet")

time.sleep(3)
driver.quit()
