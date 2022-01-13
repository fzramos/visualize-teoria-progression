from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options

def training_scraper():
    print("Starting Teoria Exercise Scraper")
    # Teoria Credentials
    load_dotenv()
    USERNAME = os.environ.get('TEORIA_USERNAME')
    PASSWORD = os.environ.get('TEORIA_PASSWORD')
    # For Windows
    # driver = webdriver.Chrome(os.getcwd() + "\chromedriver.exe")
    # For Linux (need to add geckodriver to Path first)
    driver = webdriver.Firefox(os.getcwd() + "/")

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

    # add get earliest date
    start_date = '10-11-2021'
    # TODO: This is currently hardcoded - need to intelligently click back to october month
    # Wont work 2 weeks after November
    driver.find_element_by_id("fromDate").click()
    driver.find_element_by_id("f_cal_prevMonth").click()
    driver.find_element_by_id("f_cal_w2-1").click()


    # TODO: Add clicker, while plus signs in table, click
    #   This will give you exercise info and let you eventually group by exercises
    # while driver.find_element_by_xpath("//a[@class='glyphicon glyphicon-plus-sign']"):
    # driver.find_element_by_xpath("//div[@class='glyphicon-plus-sign']").click()
    like = driver.find_elements_by_class_name('glyphicon-plus-sign')
    for x in range(0,len(like)):
        if like[x].is_displayed():
            like[x].click()

    # driver.find_element_by_xpath("//div[@class='alert alter-danger' and text()='Incorrect email or password.']")

    df = pd.read_html(driver.find_element_by_id("content").get_attribute('outerHTML'))[0]
    df['Date/time'] = pd.to_datetime(df['Date/time'])
    # TODO: test if you can just do the below code
    # dfs = pd.read_html(driver.page_source)

    driver.close()

    print('Exercise statistics from the last 7 days scraped successfully.')

    return df

if __name__ == "__main__":
    df = training_scraper()
    df.to_csv('assets/new_stats.csv', index=False)