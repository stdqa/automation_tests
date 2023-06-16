import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def products_page():
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

    # click on "Products" button
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[2]").click()
    print('Products button clicked, Done')

    # verification that "ALL PRODUCTS" is visible
    get_in_touch = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'col-sm-9 padding-right']/div[1]/h2")))
    value1 = get_in_touch.text
    assert value1 == "ALL PRODUCTS"
    print("All Products title is available , Done")

    # getting list of products for verification that they are exists
    product_list = driver.find_elements(By.XPATH, value="//div[@class = 'col-sm-4']")
    assert len(product_list) > 0
    print('Product list is not Null, Done')

    # click on view for first product
    driver.find_elements(By.XPATH, value="//div[@class = 'col-sm-4']//li/a")[0].click()
    first_product_url = 'https://automationexercise.com/product_details/1'
    assert driver.current_url == first_product_url
    print('We on first product page, Done')

    # verification that detail is visible: product name, category, price, availability, condition, brand
    product_name = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/h2").text
    product_category = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/p").text
    product_price = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/span/span").text
    product_avail = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/p[2]").text
    product_condition = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/p[3]").text
    product_brand = driver.find_element(By.XPATH, value="//div[@class = 'product-information']/p[4]").text

    if not product_name:
        print('Product is not visible, False')
    else:
        print('Product is visible, Done')

    if not product_category:
        print('Category is not visible, False')
    else:
        print('Category is visible, Done')

    if not product_price:
        print('Price is not visible, False')
    else:
        print('Price is visible, Done')

    if not product_avail:
        print('Availability is not visible, False')
    else:
        print('Availability is visible, Done')

    if not product_condition:
        print('Condition is not visible, False')
    else:
        print('Condition is visible, Done')

    if not product_brand:
        print('Brand is not visible, False')
    else:
        print('Brand is visible, Done')

    print('Test passed')
    driver.quit()


products_page()
