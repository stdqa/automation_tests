import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def scroll_up():
    service = Service(executable_path="../additional_files/geckodriver.exe")
    # options = Options()
    # options.add_argument('-headless')
    # driver.maximize_window()
    driver = webdriver.Firefox(service=service)  # , options=options)
    wait = WebDriverWait(driver, 10)

    # install adblock
    path_to_extension = os.path.join(os.getcwd(), '../additional_files/adblockultimate@adblockultimate.net.xpi')
    driver.install_addon(path_to_extension)

    # switch window
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    print('Browser is lounched, Done')

    driver.get(config.url)
    print('Main page is open, Done')

    # Verification that main page is visible
    wait.until(EC.title_contains("Automation Exercise"))
    print('Home page is visible, Done')

    # scroll down and ferify that SUBSCRIPTION is visible
    req_items = driver.find_element(By.XPATH, value="//div[@class= 'col-sm-3 col-sm-offset-1']//h2")
    text = req_items.text
    driver.execute_script("arguments[0].scrollIntoView();", req_items)
    assert text == "SUBSCRIPTION"
    print('SUBSCRIPTION is visible, Done')

    # verification
    engineers_title = driver.find_element(By.XPATH, value="//div[@id= 'slider-carousel']//div[@class  = 'col-sm-6']/h2")
    title_text = engineers_title.text
    driver.execute_script("arguments[0].scrollIntoView();", engineers_title)
    assert title_text == "Full-Fledged practice website for Automation Engineers"
    print("tittle is visible, Done")

    driver.quit()
    print('Test passed')


scroll_up()