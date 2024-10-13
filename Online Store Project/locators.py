# locators.py
from selenium.webdriver.common.by import By

class LoginPageLocators:
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

class ProductsPageLocators:
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, 'btn_inventory')
    CART_ICON = (By.CLASS_NAME, 'shopping_cart_link')
    SORT_DROPDOWN = (By.CLASS_NAME, 'product_sort_container')
    PRODUCT_PRICE = (By.CLASS_NAME, 'inventory_item_price')
    PRODUCT_NAME = (By.CLASS_NAME, 'inventory_item_name')

class CartPageLocators:
    CHECKOUT_BUTTON = (By.ID, 'checkout')

class CheckoutPageLocators:
    FIRST_NAME_INPUT = (By.ID, 'first-name')
    LAST_NAME_INPUT = (By.ID, 'last-name')
    POSTAL_CODE_INPUT = (By.ID, 'postal-code')
    CONTINUE_BUTTON = (By.ID, 'continue')
    FINISH_BUTTON = (By.ID, 'finish')
    CANCEL_BUTTON = (By.ID, 'cancel')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '.complete-header')

class MenuPageLocators:
    MENU_BUTTON = (By.ID, 'react-burger-menu-btn')
    LOGOUT_BUTTON = (By.ID, 'logout_sidebar_link')
