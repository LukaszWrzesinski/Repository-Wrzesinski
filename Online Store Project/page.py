# page.py
import time  # Import time to use time.sleep() for waiting purposes
from locators import LoginPageLocators, ProductsPageLocators, CartPageLocators, CheckoutPageLocators, MenuPageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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
        add_buttons = self.driver.find_elements(*ProductsPageLocators.ADD_TO_CART_BUTTON)
        if item_index < len(add_buttons):
            add_buttons[item_index].click()
        else:
            raise IndexError(f"Item index {item_index} is out of range. Only {len(add_buttons)} items are available.")

    def go_to_cart(self):
        self.driver.find_element(*ProductsPageLocators.CART_ICON).click()

    def sort_products(self, sort_option_text):
        sort_dropdown = Select(self.driver.find_element(*ProductsPageLocators.SORT_DROPDOWN))
        sort_dropdown.select_by_visible_text(sort_option_text)

    def get_product_prices(self):
        price_elements = self.driver.find_elements(*ProductsPageLocators.PRODUCT_PRICE)
        prices = [float(price.text.replace('$', '')) for price in price_elements]
        return prices

    def get_product_names(self):
        name_elements = self.driver.find_elements(*ProductsPageLocators.PRODUCT_NAME)
        names = [name.text for name in name_elements]
        return names


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def proceed_to_checkout(self):
        self.driver.find_element(*CartPageLocators.CHECKOUT_BUTTON).click()

    def get_cart_items(self):
        return self.driver.find_elements(By.CLASS_NAME, 'cart_item')


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_shipping_information(self, first_name, last_name, postal_code):
        self.driver.find_element(*CheckoutPageLocators.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*CheckoutPageLocators.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*CheckoutPageLocators.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.driver.find_element(*CheckoutPageLocators.CONTINUE_BUTTON).click()

    def finish_checkout(self):
        self.driver.find_element(*CheckoutPageLocators.FINISH_BUTTON).click()

    def cancel_checkout(self):
        self.driver.find_element(*CheckoutPageLocators.CANCEL_BUTTON).click()

    def get_checkout_complete_message(self):
        return self.driver.find_element(*CheckoutPageLocators.COMPLETE_HEADER).text


class MenuPage:
    def __init__(self, driver):
        self.driver = driver

    def logout(self):
        # Click the menu button and wait for the animation
        self.driver.find_element(*MenuPageLocators.MENU_BUTTON).click()
        time.sleep(1)  # Wait for menu animation to finish

        # Click the logout button
        logout_button = self.driver.find_element(*MenuPageLocators.LOGOUT_BUTTON)
        if logout_button.is_displayed():
            logout_button.click()
