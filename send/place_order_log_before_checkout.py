import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def order_log_before_checkout():
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

    # Click 'Signup / Login' button
    driver.find_element(By.XPATH, "//ul[@class='nav navbar-nav']/li[4]/a").click()

    # verification that we on correct page
    log_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'login-form']/h2")))
    value1 = log_title.text
    assert value1 == 'Login to your account'
    print('Login is available, Done')

    # find and fill form , then press button
    driver.find_element(By.XPATH, value="//input[@type = 'email']").send_keys(config.email)
    driver.find_element(By.XPATH, value="//input[@type = 'password']").send_keys(config.password)
    driver.find_element(By.XPATH, value="//button[@data-qa= 'login-button']").click()
    print('Form successfully filled, Done')

    # verification that we logged
    log_as_user = driver.find_element(By.XPATH, value="//ul[@class= 'nav navbar-nav']/li[10]/a/b").text
    assert log_as_user == config.name
    print('We logged correct, Done')

    # add product to cart and continue
    time.sleep(1)
    add_product = driver.find_element(By.XPATH, "//div[@class = 'productinfo text-center']/a")
    added_product_id = add_product.get_attribute('data-product-id')
    add_product.click()
    time.sleep(1)
    driver.find_element(By.XPATH, value="//button[@class = 'btn btn-success close-modal btn-block']").click()
    print('First product added, Done')

    # Click 'Cart' button
    driver.find_element(By.XPATH, value="//div[@class = 'shop-menu pull-right']//li[3]").click()

    # verification that cart page is displayed
    assert driver.current_url == "https://automationexercise.com/view_cart"
    print('Cart page opened, Done  ')

    # Click Proceed To Checkout
    driver.find_element(By.XPATH, value="//a[@class = 'btn btn-default check_out']").click()
    print('Clicked checkout, Done')

    # Verification Address Details and Review Your Order
    delivery_first_last = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[2]").text
    delivery_company = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[3]").text
    delivery_adr = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[4]").text
    delivery_adr2 = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[5]").text
    delivery_city_state_zip = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[6]").text
    delivery_country = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[7]").text
    delivery_phone = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[8]").text

    assert delivery_first_last == 'Mrs. ' + config.first_name + ' ' + config.last_name
    assert delivery_company == config.company
    assert delivery_adr == config.address1
    assert delivery_adr2 == config.address2
    assert delivery_city_state_zip == config.city + ' ' + config.state + ' ' + config.zip
    assert delivery_country == config.country
    assert delivery_phone == config.number

    order_id = driver.find_element(By.XPATH, value="//table[@class= 'table table-condensed']/tbody/tr[1]")
    order_id_text = order_id.get_attribute('id')
    product_number = order_id_text.split('-')[1]
    assert product_number == added_product_id
    print('Address details and product same, Done')

    # Enter description in comment text area and click 'Place Order'
    description = 'some text in description'
    driver.find_element(By.XPATH, value="//textarea[@class= 'form-control']").send_keys(description)

    driver.find_element(By.XPATH, value="//a[@class= 'btn btn-default check_out']").click()
    print('Order placed, Done')

    # Enter payment details: Name on Card, Card Number, CVC, Expiration date
    driver.find_element(By.NAME, value="name_on_card").send_keys(config.name_card)
    driver.find_element(By.NAME, value="card_number").send_keys(config.cart_number)
    driver.find_element(By.NAME, value="cvc").send_keys(config.cvc)
    driver.find_element(By.NAME, value="expiry_month").send_keys(config.exp_m)
    driver.find_element(By.NAME, value="expiry_year").send_keys(config.exp_y)

    # Click 'Pay and Confirm Order' button
    driver.find_element(By.XPATH, value="//button[@class= 'form-control btn btn-primary submit-button']").click()

    # Verify success message 'Congratulations! Your order has been confirmed!'
    success_alert = driver.find_element(By.XPATH, value="//div[@class = 'col-sm-9 col-sm-offset-1']/p").text
    assert success_alert == 'Congratulations! Your order has been confirmed!'
    print('Order payed, Done')

    # Click 'Delete Account' button
    driver.find_element(By.XPATH, "//ul[@class='nav navbar-nav']/li[5]/a").click()

    # verification that account deleted
    v_del = driver.find_element(By.XPATH, "//h2[@data-qa='account-deleted']/b").text
    assert v_del == "ACCOUNT DELETED!"
    print('Account deleted, Done')

    # click continue
    driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()
    print('Continue,  Done')

    print('Test passed')
    driver.quit()


order_log_before_checkout()
