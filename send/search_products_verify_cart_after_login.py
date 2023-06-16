import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def search_and_verify_products():
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

    # Enter product name in search input and click search button
    searched_products = 'top'
    driver.find_element(By.ID, value="search_product").send_keys(searched_products)
    driver.find_element(By.ID, value="submit_search").click()

    # Verification 'SEARCHED PRODUCTS' is visible and all products related
    searched_products_tittle = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class= 'features_items']/h2")))
    value2 = searched_products_tittle.text
    assert value2 == "SEARCHED PRODUCTS"
    all_products = driver.find_elements(By.XPATH, value="//div[@class= 'productinfo text-center']/p")
    amount_products = len(all_products)
    counter = 0
    for i in range(len(all_products)):
        if searched_products in all_products[i].text.lower():
            counter += 1
        else:
            pass
    if amount_products - 5 < counter:
        print('Most of shown products is related with searched name of product, Done')

    # Add those products to cart (only with 'top' word)
    all_add_to_cart_buttons = driver.find_elements(By.XPATH, value="//div[@class= 'productinfo text-center']/a")
    counter1 = 0
    for i in range(len(all_products)):
        if searched_products in all_products[i].text.lower():
            add_product_btn = all_add_to_cart_buttons[i]
            add_product_btn.click()
            time.sleep(1)
            continue_btn = driver.find_element(By.XPATH, value="//button[@class= 'btn btn-success close-modal btn-block']")
            continue_btn.click()
            counter1 += 1
    print('Products added, Done')

    # Click 'Cart' button and verify that products are visible in cart
    driver.find_element(By.XPATH, value="//ul[@class= 'nav navbar-nav']/li[3]").click()
    added_products = driver.find_elements(By.XPATH, value="//table[@id= 'cart_info_table']/tbody/tr")
    amount = len(added_products)
    if amount == counter1:
        print('Same amount of products shows in cart, Done')

    # Click 'Signup / Login' button and submit login details
    driver.find_element(By.XPATH, value="//ul[@class='nav navbar-nav']/li[4]/a").click()

    # verification that we on correct page
    log_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'login-form']/h2")))
    value3 = log_title.text
    assert value3 == 'Login to your account'
    print('Login is available, Done')

    # find and fill form , then press button
    driver.find_element(By.XPATH, value="//input[@type = 'email']").send_keys(config.email)
    driver.find_element(By.XPATH, value="//input[@type = 'password']").send_keys(config.password)
    driver.find_element(By.XPATH, value="//button[@data-qa= 'login-button']").click()
    print('Successfully logged, Done')

    # Again, go to Cart page and verification that those products are visible in cart after login as well
    driver.find_element(By.XPATH, value="//ul[@class= 'nav navbar-nav']/li[3]").click()
    added_products = driver.find_elements(By.XPATH, value="//table[@id= 'cart_info_table']/tbody/tr")
    amount = len(added_products)
    if amount == counter1:
        print('Same amount of products shows in cart after login, Done')

    print('Test passed')
    driver.quit()


search_and_verify_products()