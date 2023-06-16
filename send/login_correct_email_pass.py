import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

def login_correct():
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

    # find and click on signup/login
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[4]").click()

    # verification that we on correct page
    log_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'login-form']/h2")))
    value1 = log_title.text
    assert value1 == 'Login to your account'
    print('Login is available, Done')

    # find and fill form , then press button
    driver.find_element(By.XPATH, value="//input[@type = 'email']").send_keys(config.email)
    driver.find_element(By.XPATH, value="//input[@type = 'password']").send_keys(config.password)
    driver.find_element(By.XPATH, value="//button[@data-qa= 'login-button']").submit()
    print('Form successfully filled, Done')
    time.sleep(1)

    # verification that we logged
    log_as_user = driver.find_element(By.XPATH, value="//ul[@class= 'nav navbar-nav']/li[10]/a/b").text
    assert log_as_user == config.name
    print('We logged correct, Done')

    # delete account
    driver.find_element(By.XPATH, value="//ul[@class= 'nav navbar-nav']/li[5]/a").click()

    deleted = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@class='title text-center']/b")))
    value2 = deleted.text
    assert value2 == "ACCOUNT DELETED!"

    driver.find_element(By.XPATH, value="//a[@data-qa = 'continue-button']").click()
    print('Account deleted, Done')

    print('Test passed')
    driver.quit()


login_correct()
