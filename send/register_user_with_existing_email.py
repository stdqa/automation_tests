import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def existing_user():
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

    # find and click on signup/login
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[4]").click()

    # verification that we on correct page
    new_user_signup = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'signup-form']/h2")))
    value1 = new_user_signup.text
    assert value1 == "New User Signup!"
    print('Find new User Signup title, Done')

    # find and fill form with existing data , then press button
    driver.find_element(By.XPATH, value="//div[@class= 'signup-form']//input[2]").send_keys(config.name)
    driver.find_element(By.XPATH, value="//div[@class= 'signup-form']//input[3]").send_keys(config.email)
    driver.find_element(By.XPATH, value="//div[@class= 'signup-form']//button").click()
    print('Form successfully filled, Done')

    # verification that message 'Email Address already exist!' on the page under form
    error_mess = driver.find_element(By.XPATH, value="//div[@class = 'signup-form']//p").text
    assert error_mess == "Email Address already exist!"
    print('Message is correct')

    print('Test passed')
    driver.quit()


existing_user()
