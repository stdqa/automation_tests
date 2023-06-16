import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def test_cases():
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

    # click on "Test Cases" button
    driver.find_element(By.LINK_TEXT, value="Test Cases").click()
    print('Test Cases button clicked, Done')

    # verification that "GET IN TOUCH" is visible
    get_in_touch = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class = 'panel-group'][1]//span")))
    value1 = get_in_touch.text
    assert value1 == "Below is the list of test Cases for you to practice the Automation. Click on the scenario for detailed Test Steps:"
    print("Message with information is available, Done")

    print('Test passed')
    driver.quit()


test_cases()
