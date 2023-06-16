import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

def add_product_cart():
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

    # click product button
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[2]").click()
    print("Products button clicked, Done")

    # find first product and click add to cart
    all_products = driver.find_elements(By.XPATH, value="//div[@class = 'productinfo text-center']/a")
    all_products[0].click()
    print("Added first product, Done")
    time.sleep(1)

    # click continue shopping button
    driver.find_element(By.XPATH, value="//button[@class = 'btn btn-success close-modal btn-block']").click()

    # find second product and click add to cart
    all_products = driver.find_elements(By.XPATH, value="//div[@class = 'productinfo text-center']/a")
    all_products[1].click()
    print("Added second product, Done")
    time.sleep(1)
    
    # click view cart
    driver.find_element(By.XPATH, value="//div[@class = 'modal-dialog modal-confirm']//p[2]/a").click()

    # verification that 2 products added to cart
    if driver.find_elements(By.ID, value="product-1") and driver.find_elements(By.ID, value="product-2"):
        print('Two products added, Done')

    # verification prices, quantity and total price
    price_first = driver.find_element(By.XPATH, "//tr[@id = 'product-1']/td[3]/p").text
    price_second = driver.find_element(By.XPATH, "//tr[@id = 'product-2']/td[3]/p").text
    quantity_first = driver.find_element(By.XPATH, value="//tr[@id = 'product-1']/td[4]/button").text
    quantity_second = driver.find_element(By.XPATH, value="//tr[@id = 'product-2']/td[4]/button").text
    total_first = driver.find_element(By.XPATH, value="//tr[@id = 'product-1']/td[5]/p").text
    total_second = driver.find_element(By.XPATH, value="//tr[@id = 'product-2']/td[5]/p").text

    if price_second and price_first and quantity_first and quantity_second and total_first and total_second:
        print('prices, quantity and total price is visible, Done')

    print('Test passed')
    driver.quit()


add_product_cart()
