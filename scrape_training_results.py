from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import datetime

from dotenv import load_dotenv
import os


# sources
#   https://www.thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python


# Teoria Credentials
load_dotenv()
USERNAME = print(os.environ.get('USERNAME'))
PASSWORD = print(os.environ.get('PASSWORD'))

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
errors = driver.find_element_by_xpath("//div[@class='alert alter-danger' and text()='Incorrect email or password.']")
# if we find that error message within errors, then login is failed
if errors:
    print("[!] Login failed.\nCheck the username and passwork in the .env file")
else:
    print("[+] Login successful")


    # driver.find_element_by_partial_link_text(r'/app_supp_svcs/as_report_runner/report/US13/').click()
    # /app_supp_svcs/as_report_runner/report/US13/
    # Got to 2nd folder (from day before today)
    # driver.find_element_by_partial_link_text(most_recent.strftime("%Y%m%d")).click()

    # wait for next webpage to be loaded
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )

    # download files
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

    driver.find_element_by_partial_link_text('Tab-separated values').click()
    # wait for next webpage to be loaded
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )

    # driver.find_element_by_id('content_tab').click()
    # a = ActionChains(driver)
    # # do control+a
    # a.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
    # a.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()

    content = driver.find_element_by_xpath('//textarea[@class="img-responsive"]').text
    print(content)
    # TODO: only add new stats rows to permanent TSV file


driver.close()