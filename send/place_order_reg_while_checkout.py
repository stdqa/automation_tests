import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def order_while_checkout():
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

    # click on link Signup / Login and verify that tittle New User Signup is visible
    driver.find_element(By.XPATH, value="//ul[@class='nav navbar-nav']/li[4]/a").click()
    print("Click on 'Signup / Login' button, Done")

    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'signup-form']/h2")))
    new_user_signup = element.text
    assert new_user_signup == "New User Signup!"
    print('New user, Done')

    # find form elements and signup
    driver.find_element(By.XPATH, value="//input[@data-qa = 'signup-name']").send_keys(config.name)
    driver.find_element(By.XPATH, value="//input[@data-qa = 'signup-email']").send_keys(config.email)
    driver.find_element(By.XPATH, value="//button[@data-qa= 'signup-button']").submit()

    # verification that we inside
    find_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@class = 'title text-center']/b")))
    value2 = find_text.text
    assert value2 == "ENTER ACCOUNT INFORMATION"
    print('Creating account, Done')

    # checking that we can click on both gender
    driver.find_element(By.XPATH, value="//input[@id = 'id_gender1']").click()
    driver.find_element(By.XPATH, value="//input[@id = 'id_gender2']").click()

    # find elements for name, email, password, first name, last name, company, address, adr2, state, city, zip, number
    name = driver.find_element(By.XPATH, value="//input[@id = 'name']")
    if not name.get_attribute("value"):
        name.send_keys(config.name)
    # field_for_email1 = driver.find_element(by=By.XPATH, value="")
    driver.find_element(By.XPATH, value="//input[@id = 'password']").send_keys(config.password)
    driver.find_element(By.XPATH, value="//input[@id = 'first_name']").send_keys(config.first_name)
    driver.find_element(By.XPATH, value="//input[@id = 'last_name']").send_keys(config.last_name)

    # choose date of birth 9  july 2000
    # for day
    select_element_day = driver.find_element(By.ID, 'days')
    select = Select(select_element_day)
    select.select_by_value('8')

    # for month
    select_element_month = driver.find_element(By.ID, 'months')
    select1 = Select(select_element_month)
    select1.select_by_value('7')

    # for year
    select_element_year = driver.find_element(By.ID, 'years')
    select2 = Select(select_element_year)
    select2.select_by_value('2000')

    # click on 2 checkbox
    checkbox1 = driver.find_element(By.ID, 'newsletter')
    checkbox1.click()

    checkbox2 = driver.find_element(By.ID, 'optin')
    checkbox2.click()

    # scrol down to button create account
    create_acc_elem = driver.find_element(By.XPATH, value="//button[@data-qa='create-account']")
    driver.execute_script("window.scrollBy(0, 700);")

    # choose country Canada
    country = driver.find_element(By.ID, 'country')
    select3 = Select(country)
    select3.select_by_value('Canada')

    driver.find_element(By.XPATH, value="//input[@id = 'company']").send_keys(config.company)
    driver.find_element(By.XPATH, value="//input[@id = 'address1']").send_keys(config.address1)
    driver.find_element(By.XPATH, value="//input[@id = 'address2']").send_keys(config.address2)
    driver.find_element(By.XPATH, value="//input[@id = 'state']").send_keys(config.state)
    driver.find_element(By.XPATH, value="//input[@id = 'city']").send_keys(config.city)
    driver.find_element(By.XPATH, value="//input[@id = 'zipcode']").send_keys(config.zip)
    driver.find_element(By.XPATH, value="//input[@id = 'mobile_number']").send_keys(config.number)

    # submit form
    driver.execute_script("window.scrollBy(0, 400);")
    create_acc_elem.submit()

    # verification that ACCOUNT CREATED
    created = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-created']/b")))
    value3 = created.text
    assert value3 == "ACCOUNT CREATED!"
    print('Account created, Done')

    # click continue
    driver.find_element(By.XPATH, value="//a[@data-qa='continue-button']").click()

    # verification that login is correct
    logged_name = driver.find_element(By.XPATH, value="//ul[@class='nav navbar-nav']/li[10]/a/b").text
    assert logged_name == config.name
    print('Name is correct, Done')

    # Click 'Cart' button and proceed to checkout button
    driver.find_element(By.XPATH, value="//div[@class = 'shop-menu pull-right']//li[3]").click()
    driver.find_element(By.XPATH, value="//a[@class = 'btn btn-default check_out']").click()

    # Verification Address Details and Review Your Order
    delivery_first_last = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[2]").text
    delivery_company = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[3]").text
    delivery_adr = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[4]").text
    delivery_adr2 = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[5]").text
    delivery_city_state_zip = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[6]").text

    delivery_country = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[7]").text
    delivery_phone = driver.find_element(By.XPATH, value="//ul[@id= 'address_delivery']/li[8]").text

    assert delivery_first_last == f'Mrs. {config.first_name} {config.last_name}'
    assert delivery_company == config.company
    assert delivery_adr == config.address1
    assert delivery_adr2 == config.address2
    assert delivery_city_state_zip == f'{config.city} {config.state} {config.zip}'
    assert delivery_country == config.country
    assert delivery_phone == config.number

    order_id = driver.find_element(By.XPATH, value="//table[@class= 'table table-condensed']/tbody/tr[1]")
    order_id_text = order_id.get_attribute('id')
    product_number = order_id_text.split('-')[1]
    assert product_number == added_product_id
    print('Address details and product same, Done')

    # Enter description in comment text area and click 'Place Order'
    description = 'some test in description'
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


order_while_checkout()
