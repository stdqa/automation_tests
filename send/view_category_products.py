import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def category_products():
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

    # Verification that categories are visible on left sidebar
    category = driver.find_element(By.XPATH, value="//div[@class= 'panel-group category-products']").text
    if category:
        print('Category is not empty, Done')

    # Click on 'Women' category
    women = driver.find_element(By.XPATH, value="//div[@class = 'panel-heading']/h4[1]/a")
    women_text = women.text
    women.click()

    # Click on any category link under 'Women' category, for example: Dress
    dress = driver.find_element(By.XPATH, value="//div[@id= 'Women']//li[1]/a")
    dress1 = dress.text
    dress.click()

    # Verify that category page is displayed and confirm text 'WOMEN - TOPS PRODUCTS'
    tittle = driver.find_element(By.XPATH, value="//h2[@class= 'title text-center']").text
    a = f'{women_text} - {dress1} PRODUCTS'
    assert tittle == a
    print('Women info correct, Done')

    # On left sidebar, click on any sub-category link of 'Men' category
    men_text = driver.find_element(By.XPATH, value="//div[@id= 'accordian']/div[2]//a[1]")
    men1 = men_text.text
    men_text.click()
    sub_men = driver.find_element(By.XPATH, value="//div[@id= 'Men']//li[2]/a")
    sub_men1 = sub_men.text
    sub_men.click()

    # Verification that user is navigated to that category page
    b = f'{men1} - {sub_men1} PRODUCTS'
    tittle1 = driver.find_element(By.XPATH, value="//h2[@class= 'title text-center']").text
    assert tittle1 == b
    print('Men info correct, Done')

    print('Test passed')
    driver.quit()


category_products()