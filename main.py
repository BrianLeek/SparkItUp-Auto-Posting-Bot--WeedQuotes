import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from quotes import quotes
import random
import config
import time
import sys

options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2} # Press "Allow" on the notifications popup.
options.add_experimental_option("prefs", prefs)
options.add_argument("--no-sandbox")
options.headless = config.headless # Run script in headless mode or not. Uses value from config.py.

driver = webdriver.Chrome(executable_path=config.driverpath,chrome_options=options) # Path to the webdriver set in config.py.
driver.get(config.website)

time.sleep(2)

try:
    print("Logging in...")
    accept_cookies = driver.find_element_by_class_name("cc-btn").click()

    login_username = driver.find_element_by_name("username")
    login_username.click()
    login_username.send_keys(config.username)

    login_password = driver.find_element_by_name("password")
    login_password.click()
    login_password.send_keys(config.password)

    driver.find_element_by_xpath('//button[@type="submit"]').click()

    print("Successfully logged in.")

    time.sleep(2)

    # confirm_code = driver.find_element_by_name("confirm_code")
    # if confirm_code:
    #     confirm_code.click()
    #     confirmation_code = input("Confirmation Code: ")
    #     driver.find_element_by_xpath('//button[@type="submit"]').click()
    # else:
    #     pass
except ValueError:
    print("Couldn't login with the infomation given. Please check your username and password and try again.")
    sys.exit()

time.sleep(3)

try:
    if config.page_name:
        driver.get(f"{config.website}{config.page_name}")
    else:
        pass

    while config.send_posts:
        new_post_box = driver.find_element_by_xpath("//button[@data-target='#tagPostBox']")
        new_post_box.click()

        time.sleep(1)

        post_box = driver.find_element_by_name("postText")
        post_box.click()

        random_quote = random.choice(quotes)
        post_box.send_keys(random_quote)

        driver.find_element_by_id("publisher-button").click()

        time.sleep(config.time_between)
except ValueError:
    print(f"Couldn't send post. Will try again in {config.time_between} seconds.")

driver.find_element_by_xpath('//button[@type="button"]').click()
