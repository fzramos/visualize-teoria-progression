from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
import pandas as pd
import time

def training_scraper():
    # Teoria Credentials
    load_dotenv()
    USERNAME = os.environ.get('TEORIA_USERNAME')
    PASSWORD = os.environ.get('TEORIA_PASSWORD')

    # initialize the Chrome driver
    driver = webdriver.Chrome("chromedriver")

    # Login
    driver.get("https://www.teoria.com/en/members/index.php?url=/en/exercises/ie.php")
    # find username/email field and send the username itself to the input field
    driver.find_element_by_id("email").send_keys(USERNAME)
    # find password input field and insert password as well
    driver.find_element_by_id("ord_pwd").send_keys(PASSWORD)
    # click login button
    driver.find_element_by_name("sign_in").click()

    # wait the ready state to be complete
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    # get the errors (if login fails)
    # errors = driver.find_element_by_xpath("//div[@class='alert alter-danger' and text()='Incorrect email or password.']")

    # TODO: ERROR HANDLING
    # if we find that error message within errors, then login is failed
    # if errors:
    #     print("[!] Login failed.\nCheck the username and passwork in the .env file")
    # else:
    #     print("[+] Login successful")

    driver.find_element_by_partial_link_text(USERNAME).click()
    # wait for next webpage to be loaded
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )

    driver.find_element_by_partial_link_text('Scores and Graphs').click()
    # wait for next webpage to be loaded
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )

    # need this to let page load table
    time.sleep(3)

    df = pd.read_html(driver.find_element_by_id("content").get_attribute('outerHTML'))[0]
    # TODO: test if you can just do the below code
    # dfs = pd.read_html(driver.page_source)

    df.to_csv('stats.csv', index=False)

    # TODO: only add new stats rows to permanent CSV file

    driver.close()

if __name__ == "__main__":
    training_scraper()