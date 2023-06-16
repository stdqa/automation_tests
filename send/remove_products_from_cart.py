import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def remove_from_cart():
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

    # add product to cart and continue
    driver.find_element(By.XPATH, "//div[@class = 'productinfo text-center']/a").click()
    time.sleep(1)
    driver.find_element(By.XPATH, value="//button[@class = 'btn btn-success close-modal btn-block']").click()
    print('First product added, Done')

    # Click 'Cart' button
    driver.find_element(By.XPATH, value="//div[@class = 'shop-menu pull-right']//li[3]").click()

    # verification that cart page is displayed
    assert driver.current_url == "https://automationexercise.com/view_cart"
    print('Cart page opened, Done  ')

    # Click 'X' button corresponding to particular product
    driver.find_element(By.XPATH, "//a[@class = 'cart_quantity_delete']").click()
    time.sleep(1)

    # verification that product is removed from the cart
    empty = driver.find_element(By.XPATH, "//span[@id = 'empty_cart']/p/b").text
    assert empty == "Cart is empty!"
    print('Product deleted, Done')

    print('Test passed')
    driver.quit()



remove_from_cart()