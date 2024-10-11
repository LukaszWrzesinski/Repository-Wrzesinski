import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from locators import RegistrationPageLocators, MainPageLocators
from page import BasePage
from element import BaseElement

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def register(self, first_name="John", last_name="Doe", address="123 Main St", city="Testville",
                 state="TS", zip_code="12345", phone="1234567890", ssn="123-45-6789",
                 username="testuser8", password="password123"):
        # Navigate to registration page
        self.find_element(RegistrationPageLocators.REGISTER_LINK).click()

        # Fill in registration form
        self.find_element(RegistrationPageLocators.FIRST_NAME_FIELD).send_keys(first_name)
        self.find_element(RegistrationPageLocators.LAST_NAME_FIELD).send_keys(last_name)
        self.find_element(RegistrationPageLocators.ADDRESS_FIELD).send_keys(address)
        self.find_element(RegistrationPageLocators.CITY_FIELD).send_keys(city)
        self.find_element(RegistrationPageLocators.STATE_FIELD).send_keys(state)
        self.find_element(RegistrationPageLocators.ZIP_CODE_FIELD).send_keys(zip_code)
        self.find_element(RegistrationPageLocators.PHONE_FIELD).send_keys(phone)
        self.find_element(RegistrationPageLocators.SSN_FIELD).send_keys(ssn)
        self.find_element(RegistrationPageLocators.USERNAME_FIELD).send_keys(username)
        self.find_element(RegistrationPageLocators.PASSWORD_FIELD).send_keys(password)
        self.find_element(RegistrationPageLocators.REPEATED_PASSWORD_FIELD).send_keys(password)

        # Submit registration form
        register_button = self.find_element(RegistrationPageLocators.REGISTER_BUTTON)
        register_button.click()

        # Wait for either confirmation or an error message
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(RegistrationPageLocators.LOGOUT_LINK)
            )
        except TimeoutException:
            # Handle the case where registration fails (e.g., username already exists)
            error_message = self.find_element((By.XPATH, "//span[contains(text(), 'This username already exists.')]")).text
            raise AssertionError(f"Registration failed with error: {error_message}")

    def logout(self):
        # Click on the logout link to log out
        logout_link = self.find_element(RegistrationPageLocators.LOGOUT_LINK)
        logout_link.click()
        # Wait for the login page or another confirmation element to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.LOGIN_BUTTON)
        )
    def login(self, username, password):
        # Fill in login form
        self.find_element(MainPageLocators.USERNAME_FIELD).send_keys(username)
        self.find_element(MainPageLocators.PASSWORD_FIELD).send_keys(password)
        # Click login button
        self.find_element(MainPageLocators.LOGIN_BUTTON).click()
        # Wait for account overview page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.ACCOUNTS_OVERVIEW_LINK)
        )


class PythonOrgSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up once for the whole test suite
        service = Service("/home/lukasz/chromedriver-linux64/chromedriver")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.get("https://parabank.parasoft.com/")
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)  # Implicit wait for elements to load
        cls.main_page = MainPage(cls.driver)

    def test_open_website(self):
        driver = self.driver
        # Verifying that the correct page is loaded
        self.assertIn("ParaBank", driver.title)

    def test_register(self):
        # Register a user with default data
        self.main_page.register()
        # Check if registration was successful by verifying the presence of the logout link
        self.assertTrue(
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(RegistrationPageLocators.LOGOUT_LINK)
            ).is_displayed()
        )
        # Log out after registration
        self.main_page.logout()

    def test_register_existing_user(self):
        # Register a user with specific data
        try:
            self.main_page.register()
        except AssertionError as e:
            self.fail(f"First registration failed unexpectedly: {str(e)}")
        # Log out after successful registration
        self.main_page.logout()
        # Attempt to register the same user again with the same data
        with self.assertRaises(AssertionError) as context:
            self.main_page.register()
        # Verify that the exception message contains information about the username already existing
        self.assertIn("This username already exists.", str(context.exception))

    def test_login_after_registration(self):
        username = "testuser9"
        password = "password128"
        self.main_page.register(first_name="John", last_name="Doe", address="123 Main St", city="Testville",
                                state="TS", zip_code="12345", phone="1234567890", ssn="123-45-6789",
                                username=username, password=password)

        # Log out after registration
        self.main_page.logout()
        # Login with the same credentials
        self.main_page.login(username=username, password=password)
        # Check if login was successful by verifying the presence of the accounts overview link
        self.assertTrue(
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(MainPageLocators.ACCOUNTS_OVERVIEW_LINK)
            ).is_displayed()
        )
    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()
