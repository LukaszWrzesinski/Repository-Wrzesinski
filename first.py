from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Path to your ChromeDriver
PATH = "/home/lukasz/chromedriver-linux64/chromedriver"
# Create an instance of ChromeOptions
options = Options()
# Create a Service object
service = Service(executable_path=PATH)
# Initialize the Chrome WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=options)
# Open the desired webpage
driver.get("https://cip-ui.service.cip3x-qa/")
driver.implicitly_wait(10)


try:
    element = WebDriverWait (driver, 20).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    element.send_keys("admin")
    element = driver.find_element(By.ID,"password")
    element.send_keys("1qaz2wsx")
    element.send_keys(Keys.RETURN)

    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "input_0"))
    )
    element.send_keys("971216840155")
    element.send_keys(Keys.RETURN)

    driver.back()

except Exception as e:
    print(f"Error: {e}")
    driver.quit()





