# page.py
from locators import LoginPageLocators, ProductsPageLocators
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(*LoginPageLocators.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.error-message-container').text


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def add_item_to_cart(self, item_index=0):
        # Add item to cart by index (assuming items are listed in order)
        add_buttons = self.driver.find_elements(*ProductsPageLocators.ADD_TO_CART_BUTTON)
        add_buttons[item_index].click()

    def go_to_cart(self):
        self.driver.find_element(*ProductsPageLocators.CART_ICON).click()


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def proceed_to_checkout(self):
        self.driver.find_element(By.ID, 'checkout').click()

    def get_cart_items(self):
        # Get all items listed in the cart
        return self.driver.find_elements(By.CLASS_NAME, 'cart_item')


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_shipping_information(self, first_name, last_name, postal_code):
        self.driver.find_element(By.ID, 'first-name').send_keys(first_name)
        self.driver.find_element(By.ID, 'last-name').send_keys(last_name)
        self.driver.find_element(By.ID, 'postal-code').send_keys(postal_code)
        self.driver.find_element(By.ID, 'continue').click()

    def finish_checkout(self):
        self.driver.find_element(By.ID, 'finish').click()

    def cancel_checkout(self):
        # Click the Cancel button to abort the checkout process
        self.driver.find_element(By.ID, 'cancel').click()

    def get_checkout_complete_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.complete-header').text
