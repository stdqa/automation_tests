import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


def add_review():
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
    print('Browser is launched, Done')

    driver.get(config.url)
    print('Main page is open, Done')

    # Verification that main page is visible
    wait.until(EC.title_contains("Automation Exercise"))
    print('Home page is visible, Done')

    # Click on 'Products' button
    driver.find_element(By.XPATH, value="//ul[@class='nav navbar-nav']/li[2]/a").click()

    # Verification that navigated to ALL PRODUCTS page successfully
    all_products_tittle = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@class= 'title text-center']")))
    value1 = all_products_tittle.text
    assert value1 == 'ALL PRODUCTS'
    print('Tittle is correct')

    # Click on 'View Product' button and Verify 'Write Your Review' is visible
    driver.find_element(By.XPATH, value="//div[@class= 'choose']//a").click()
    write_review_tittle = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class= 'col-sm-12']//a")))
    value2 = write_review_tittle.text
    assert value2 == 'WRITE YOUR REVIEW'
    print("Write Your Review tittle is visible, Done")

    # Enter name, email and review and click submit
    driver.find_element(By.ID, value="email").send_keys(config.email)
    driver.find_element(By.ID, value="name").send_keys(config.name)
    driver.find_element(By.ID, value="review").send_keys(config.review)
    driver.find_element(By.ID, value="button-review").click()

    success_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class= 'alert-success alert']/span")))
    value3 = success_msg.text
    assert value3 == "Thank you for your review."
    print('Message is visible, Done')

    print('Test passed')
    driver.quit()

add_review()
