from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime, timedelta
import sys
import os
import logging
logging.getLogger('selenium').setLevel(logging.WARNING)

# HAYDEN_LIBRARY_WEBSITE = "https://asu.libcal.com/reserve/hayden-study" # "https://asu.libcal.com/space/108068"
ROOM_NUMBER = "C19"
# RESERVE_TIME = datetime(2024, 10, 13, 23, 0) # year, month, day, hour (0-24), minute 
USERNAME = os.getenv("ASU_USER")
PASSWORD = os.getenv("ASU_PASS")
ASU_ID = os.getenv("ASU_ID")

def reserve_library(room_number, reserve_time, username, password, asu_id):
    options = ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get("https://asu.libcal.com/reserve/hayden-study")

    time_str = reserve_time.strftime("%A, %B") + f" {reserve_time.day}, {reserve_time.year}"
    print(f"Finding date ({time_str})...")
    while time_str not in driver.page_source:
        print("clicking Next button")
        button = driver.find_element(By.XPATH, '//button[@class="fc-next-button btn btn-default btn-sm"]')
        button.click()
    a_tags = driver.find_elements(By.TAG_NAME, 'a')

    time_format = "%I:%M %p %A, %B" + f" {reserve_time.day}, {reserve_time.year}"
    time_wanted = reserve_time.strftime(time_format).replace("AM", "am").replace("PM", "pm")
    print(f"Checking if time is available ({time_wanted})...")
    test = ""
    for a_tag in a_tags:
        test = a_tag.get_attribute('title')
        if room_number in test:
            print(test)
            if time_wanted in test:
                if "Unavailable" in test:
                    print("Time unavailable.")
                    raise Exception("Time unavailable")
                a_tag.click()
                break

    print("Submitting times...")
    wait = WebDriverWait(driver, 30)
    button = wait.until(EC.element_to_be_clickable((By.ID, "submit_times")))
    button.click()

    print("Logging in...")
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.send_keys(username)

    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
    login_button.click()

    print("Waiting for Duo push to be confirmed...")
    trust_browser_button = wait.until(EC.element_to_be_clickable((By.ID, "trust-browser-button")))
    trust_browser_button.click()

    print("Confirming information release...")
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]')))
    accept_button.click()

    print("Submitting times...")
    asu_id_field = wait.until(EC.presence_of_element_located((By.ID, "q1546")))
    asu_id_field.send_keys(asu_id)

    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-form-submit")))
    submit_button.click()

    print("Submitted. Check email for confirmation")


if __name__ == "__main__":
    now = datetime.now()
    next_available_date = now + timedelta(days=7)
    RESERVE_TIME = next_available_date.replace(hour=13, minute=0, second=0, microsecond=0)

    reserve_library(ROOM_NUMBER, RESERVE_TIME, USERNAME, PASSWORD, ASU_ID)