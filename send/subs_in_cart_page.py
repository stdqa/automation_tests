import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def cart_subscription():
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

    # click 'cart' button
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[3]").click()
    print('Clicked on cart button, Done')

    # scroll down to footer
    footer = driver.find_element(By.CLASS_NAME, value="footer-bottom")
    #ActionChains(driver).move_to_element(footer).perform()
    driver.execute_script("arguments[0].scrollIntoView();", footer)

    # verification text SUBSCRIPTION
    sub = driver.find_element(By.XPATH, "//div[@class = 'single-widget']/h2").text
    assert sub == 'SUBSCRIPTION'
    print("SUBSCRIPTION, Done")

    # enter email and follow
    email_field = driver.find_element(By.ID, value="susbscribe_email")
    email_field.send_keys(config.email)

    driver.find_element(By.ID, value="subscribe").click()

    # verification You have been successfully subscribed! message is visible
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class = 'alert-success alert']").text
    assert message == 'You have been successfully subscribed!'

    print('Test passed')
    driver.quit()


cart_subscription()
