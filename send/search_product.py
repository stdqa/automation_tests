import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def search_products():
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

    # click on "Products" button
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[2]").click()
    print('Products button clicked, Done')

    # verification that "ALL PRODUCTS" is visible
    get_in_touch = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'col-sm-9 padding-right']/div[1]/h2")))
    value1 = get_in_touch.text
    assert value1 == "ALL PRODUCTS"
    print("All Products title is available , Done")

    # input 'top' in search field and search
    key = 'top'
    driver.find_element(By.ID, value="search_product").send_keys(key)
    driver.find_element(By.ID, value="submit_search").click()

    # verification that searched product is visible
    searched_product = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@class = 'title text-center']")))
    value2 = searched_product.text
    assert value2 == 'SEARCHED PRODUCTS'
    print('Searched product is visible, Done')

    # verification that searched product is related to 'top' and visible
    all_products = driver.find_elements(By.XPATH, value="//div[@class = 'productinfo text-center']")

    for i in range(len(all_products)):
        product_name = all_products[i].find_element(By.XPATH, "./p").text
        if key in product_name:
            print('Products related to search are visible, Done')


    print('Test passed')
    driver.quit()


search_products()
