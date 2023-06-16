import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def cart_from_recommended():
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

    # Scroll down and verify recommended items
    req_items = driver.find_element(By.XPATH, value="//div[@class= 'recommended_items']/h2")
    req_items_text = req_items.text
    driver.execute_script("arguments[0].scrollIntoView();", req_items)
    assert req_items_text == "RECOMMENDED ITEMS"
    print('Scrolled down, Done')

    # Click on 'Add To Cart' on Recommended product
    product_btn = driver.find_element(By.XPATH, value="//div[@class= 'item active']//a[@class = 'btn btn-default add-to-cart']")
    id = product_btn.get_attribute('data-product-id')
    product_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, value="//div[@class= 'modal-body']//a").click()
    print('Added product to cart, Done')

    # Verification that same product in the cart
    id_in_cart = driver.find_element(By.XPATH, value="//table[@id= 'cart_info_table']/tbody/tr")
    id2 = id_in_cart.get_attribute('id')
    assert id == id2[-1:]
    print('Product same, Done')

    driver.quit()
    print('Test passed')


cart_from_recommended()
