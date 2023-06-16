import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def contact_us():
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

    # click on "Contact us" button
    driver.find_element(By.XPATH, value="//ul[@class = 'nav navbar-nav']/li[8]").click()
    print('Contact us button clicked, Done')

    # verification that "GET IN TOUCH" is visible
    get_in_touch = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'contact-form']/h2")))
    value1 = get_in_touch.text
    assert value1 == "GET IN TOUCH"
    print("GET IN TOUCH is available, Done")

    # enter name, email, subject and message in the form
    driver.find_element(By.XPATH, value="//div[@class = 'form-group col-md-6'][1]/input").send_keys(config.name)
    driver.find_element(By.XPATH, value="//div[@class = 'form-group col-md-6'][2]/input").send_keys(config.email)
    driver.find_element(By.XPATH, value="//div[@class = 'form-group col-md-12'][1]/input").send_keys(config.subject)
    driver.find_element(By.XPATH, value="//div[@class = 'form-group col-md-12'][2]/textarea").send_keys(config.message)

    # upload file test.txt, file in the same directory
    file_path = os.path.join(os.getcwd(), '../additional_files/test.txt')
    driver.find_element(By.NAME, value="upload_file").send_keys(file_path)
    driver.find_element(By.NAME, value="submit").submit()
    print('Button is submitted, Done')
    time.sleep(1)

    # press ok on alert window
    driver.switch_to.alert.accept()

    # verification that success message is Success! Your details have been submitted successfully. is visible
    success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'status alert alert-success']")))
    value2 = success_message.text
    assert value2 == "Success! Your details have been submitted successfully."
    print('Success message found, Done')

    # click on home button and verification that we on main page
    driver.find_element(By.XPATH, value="//a[@class = 'btn btn-success']").click()
    wait.until(EC.title_contains('Automation Exercise'))
    print('Home page is visible, Done')

    print('Test passed')
    driver.quit()


contact_us()
