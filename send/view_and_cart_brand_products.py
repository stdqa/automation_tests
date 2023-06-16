import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def brand_products():
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

    # Click on 'Products' button
    driver.find_element(By.XPATH, "//ul[@class='nav navbar-nav']/li[2]/a").click()

    # Verification  that Brands are visible on left sidebar
    brands = driver.find_element(By.XPATH, value="//ul[@class= 'nav nav-pills nav-stacked']").text
    if brands:
        print('Brands is not empty, Done')

    # Click on any brand name
    third_brand_name = driver.find_element(By.XPATH, value="//div[@class = 'brands-name']/ul/li[3]/a")
    third_brand_name1 = third_brand_name.text
    third_brand_name.click()

    # Verification that user is navigated to brand page and brand products are displayed
    brand_tittle = driver.find_element(By.XPATH, value="//div[@class = 'features_items']/h2").text
    assert brand_tittle == f'BRAND - {third_brand_name1[4:]} PRODUCTS'
    print('Correct page, Done')

    # On left sidebar, click on any other brand link and verify that
    second_brand_name = driver.find_element(By.XPATH, value="//div[@class = 'brands-name']/ul/li[2]/a")
    second_brand_name1 = second_brand_name.text
    second_brand_name.click()
    brand_tittle = driver.find_element(By.XPATH, value="//div[@class = 'features_items']/h2").text
    assert brand_tittle == f'BRAND - {second_brand_name1[4:]} PRODUCTS'
    print('Correct page, Done')

    print('Test passed')
    driver.quit()


brand_products()
