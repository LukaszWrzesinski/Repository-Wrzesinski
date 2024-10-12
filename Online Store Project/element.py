from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class WebDriverSetup:
    def __init__(self):
        # Setup Chrome WebDriver with the Service method to specify the ChromeDriver path
        service = Service('/home/lukasz/chromedriver-linux64/chromedriver')
        self.driver = webdriver.Chrome(service=service)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.quit()
