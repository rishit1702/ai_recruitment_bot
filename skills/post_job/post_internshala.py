import os
import sys
import time
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv(os.path.expanduser("~/Desktop/ai_recruitment_bot/.env"))

def run(role="PHP Developer", location="Mumbai", experience="5", description="", count="3", skills=["PHP", "Laravel", "MySQL"]):
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=/tmp/chrome_internshala_profile")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-extensions")
        options.add_argument("--profile-directory=.")

        driver = uc.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        driver.get("https://internshala.com/job/form")
        time.sleep(5)
        print("Page loaded:", driver.current_url)

        # Select Job tab
        job_btn = wait.until(EC.presence_of_element_located((By.ID, "job_form_btn_2")))
        driver.execute_script("arguments[0].click();", job_btn)
        time.sleep(2)

        # Job title
        title = wait.until(EC.presence_of_element_located((By.ID, "job_title")))
        title.clear()
        title.send_keys(role)
        time.sleep(1)
        try:
            suggestion = driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete .ui-menu-item")
            suggestion.click()
        except:
            pass
        time.sleep(1)

        # Experience
        if int(experience) >= 1:
            exp_radio = driver.find_element(By.ID, "min_experience_2")
            driver.execute_script("arguments[0].click();", exp_radio)
        time.sleep(1)

        # Skills
        for skill in skills:
            skill_input = driver.find_element(By.ID, "job_skill")
            skill_input.clear()
            skill_input.send_keys(skill)
            time.sleep(1)
            try:
                suggestion = driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete .ui-menu-item")
                suggestion.click()
            except:
                skill_input.send_keys(Keys.ENTER)
            time.sleep(1)

        # Job type - In office
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "job_type_regular"))
        time.sleep(1)

        # Full time
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "full_time_job"))
        time.sleep(1)

        # Location
        loc = driver.find_element(By.ID, "job_location")
        loc.clear()
        loc.send_keys(location)
        time.sleep(2)
        try:
            suggestion = driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete .ui-menu-item")
            suggestion.click()
        except:
            pass
        time.sleep(1)

        # Number of openings
        openings = driver.find_element(By.ID, "job_open_positions")
        openings.clear()
        openings.send_keys(count)
        time.sleep(1)

        # Job description
        desc = driver.find_element(By.ID, "job_description")
        desc.clear()
        desc.send_keys(description)
        time.sleep(1)

        # Salary
        driver.find_element(By.ID, "job_salary").send_keys("500000")
        driver.find_element(By.ID, "job_salary2").send_keys("1000000")
        time.sleep(1)

        # Screenshot before submit
        driver.save_screenshot("/tmp/before_submit.png")
        print("Form filled. Screenshot at /tmp/before_submit.png")

        # Guidelines checkbox
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "important_guidelines_checkbox"))
            time.sleep(1)
        except:
            pass

        # Submit
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "submit"))
        time.sleep(5)

        print("After submit URL:", driver.current_url)
        driver.save_screenshot("/tmp/after_submit.png")

        return "✅ Job posted successfully on Internshala!\n\n🧾 " + role + " — " + location + "\n👥 " + count + " openings\n📋 Candidates can now apply directly\n\n---\n✅ Want me to notify you when applicants come in?"

    except Exception as e:
        if driver:
            driver.save_screenshot("/tmp/error.png")
        return "❌ Posting failed: " + str(e)
    finally:
        if driver:
            time.sleep(3)
            driver.quit()

if __name__ == "__main__":
    print(run())
