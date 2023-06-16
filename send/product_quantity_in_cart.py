import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def quantity_product_cart():
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

    # click view product button for first product
    driver.find_element(By.XPATH, value="//div[@class='choose']//a").click()
    print("View 1st product button clicked, Done")

    # verification that product detail is opened
    product_info = driver.find_element(By.XPATH, value="//div[@class='product-information']").text
    if product_info:
        print('Information is visible, Done')

    # increase quantity to 4
    quantity = driver.find_element(By.ID, value="quantity")
    quantity.clear()
    quantity.send_keys(4)

    # Click 'Add to cart' button
    driver.find_element(By.XPATH, value="//button[@class = 'btn btn-default cart']").click()
    time.sleep(1)

    # click view cart
    driver.find_element(By.XPATH, value="//div[@class = 'modal-dialog modal-confirm']//p[2]/a").click()

    # verification that 2 products added to cart
    if driver.find_elements(By.ID, value="product-1"):
        print('Product added, Done')

    quantity_first = driver.find_element(By.XPATH, value="//tr[@id = 'product-1']/td[4]/button").text
    if quantity_first == 4:
        print('Product added with correct quantity, Done')

    print('Test passed')
    driver.quit()


quantity_product_cart()
