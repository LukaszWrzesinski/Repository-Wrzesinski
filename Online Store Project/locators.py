from selenium.webdriver.common.by import By

class LoginPageLocators:
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

class ProductsPageLocators:
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, 'btn_inventory')
    CART_ICON = (By.CLASS_NAME, 'shopping_cart_link')
