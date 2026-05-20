import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os

# Read JD from file saved by Telegram bot
jd_file = "/tmp/last_jd.json"
if os.path.exists(jd_file):
    with open(jd_file) as f:
        jd_data = json.load(f)
    role = jd_data.get("role", "Software Engineer")
    location = jd_data.get("location", "Mumbai")
    experience = jd_data.get("experience", "5")
    count = jd_data.get("count", "3")
    skills = jd_data.get("skills", "Software Developer")
    description = jd_data.get("description", "")
    print(f"Loaded JD: {role} in {location}")
else:
    # Fallback defaults
    role = "Software Engineer"
    skills = "Software Developer"
    location = "Mumbai"
    experience = "5"
    count = "3"
    description = "We are hiring PHP Developers for VVDN Technologies. PHP 8, Laravel, MySQL required. Mumbai. Full-time."
    print("No JD file found, using defaults")

options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/tmp/chrome_internshala_profile")
options.add_argument("--no-first-run")
options.add_argument("--disable-extensions")
options.add_argument("--profile-directory=.")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

def js_fill_input(field_id, value):
    driver.execute_script("""
        var el = document.getElementById(arguments[0]);
        var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, arguments[1]);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    """, field_id, value)

def js_fill_textarea(field_id, value):
    driver.execute_script("""
        var el = document.getElementById(arguments[0]);
        var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, arguments[1]);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    """, field_id, value)

driver.get("https://internshala.com/job/form")
time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)

# Select Job tab
driver.execute_script("arguments[0].click();", wait.until(EC.presence_of_element_located((By.ID, "job_form_btn_1"))))
time.sleep(2)

# Job title
title = wait.until(EC.presence_of_element_located((By.ID, "job_title")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", title)
title.send_keys(role)
time.sleep(1)
try:
    driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete li:first-child").click()
except:
    pass
time.sleep(1)

# Experience
driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "min_experience_2"))
time.sleep(1)

# Skills
for skill in [s.strip() for s in skills.split(",")][:5]:
    s = driver.find_element(By.ID, "job_skill")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", s)
    s.clear()
    s.send_keys(skill)
    time.sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete li:first-child").click()
    except:
        s.send_keys(Keys.ENTER)
    time.sleep(1)

# Job type
driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "job_type_regular"))
time.sleep(1)

# Full time
driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "full_time_job"))
time.sleep(1)

# Location
loc = driver.find_element(By.ID, "job_location")
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", loc)
driver.execute_script("arguments[0].click();", loc)
time.sleep(1)
driver.execute_script("""
    var el = document.getElementById('job_location');
    el.focus();
    el.value = arguments[0];
    el.dispatchEvent(new KeyboardEvent('keydown', {bubbles:true}));
    el.dispatchEvent(new Event('input', {bubbles:true}));
    el.dispatchEvent(new KeyboardEvent('keyup', {bubbles:true}));
""", location)
time.sleep(3)
loc.send_keys(Keys.ARROW_DOWN)
time.sleep(1)
loc.send_keys(Keys.ENTER)
time.sleep(1)

# Openings
openings = driver.find_element(By.ID, "job_open_positions")
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", openings)
openings.send_keys(count)
time.sleep(1)

# Description
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", driver.find_element(By.ID, "job_description"))
time.sleep(1)
clean_desc = description.replace(chr(0x202f), ' ').replace(chr(0x2011), '-').replace(chr(0x2013), '-').replace(chr(0x2019), "'").replace(chr(0x00a0), ' ').replace('•', '-')
js_fill_textarea("job_description", clean_desc)
time.sleep(2)

# CTC
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
js_fill_input("job_salary", "1200000")
js_fill_input("job_salary2", "1800000")
js_fill_input("variable_salary", "100000")
js_fill_input("variable_salary2", "200000")
time.sleep(1)

# No AI interview
try:
    no_ai = driver.find_element(By.ID, "disable_ai_screening_job")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", no_ai)
    driver.execute_script("arguments[0].click();", no_ai)
    time.sleep(1)
except:
    pass

# Guidelines
try:
    cb = driver.find_element(By.ID, "important_guidelines_checkbox")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
    driver.execute_script("arguments[0].click();", cb)
    time.sleep(1)
except:
    pass

driver.save_screenshot("/tmp/before_submit.png")
print("Form filled with JD from Telegram. Pausing 40 seconds.")
time.sleep(3)

# SUBMIT - uncomment for real demo
buttons = driver.find_elements(By.TAG_NAME, "button")
for b in buttons:
    print("BUTTON:", repr(b.text), "ID:", b.get_attribute("id"), "class:", b.get_attribute("class"))
post_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_btn")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_btn)
time.sleep(1)
driver.execute_script("arguments[0].click();", post_btn)
time.sleep(3)
print("Job posted!")
# time.sleep(6)
# print("Final URL:", driver.current_url)

driver.quit()
print("Done")
