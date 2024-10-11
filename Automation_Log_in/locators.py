from selenium.webdriver.common.by import By

class RegistrationPageLocators:
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FIRST_NAME_FIELD = (By.ID, "customer.firstName")
    LAST_NAME_FIELD = (By.ID, "customer.lastName")
    ADDRESS_FIELD = (By.ID, "customer.address.street")
    CITY_FIELD = (By.ID, "customer.address.city")
    STATE_FIELD = (By.ID, "customer.address.state")
    ZIP_CODE_FIELD = (By.ID, "customer.address.zipCode")
    PHONE_FIELD = (By.ID, "customer.phoneNumber")
    SSN_FIELD = (By.ID, "customer.ssn")
    USERNAME_FIELD = (By.ID, "customer.username")
    PASSWORD_FIELD = (By.ID, "customer.password")
    REPEATED_PASSWORD_FIELD = (By.ID, "repeatedPassword")
    REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
    LOGOUT_LINK = (By.LINK_TEXT, "Log Out")

class MainPageLocators:
    # Keeping these locators in case they are needed for other actions in the future
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    ACCOUNTS_OVERVIEW_LINK = (By.LINK_TEXT, "Accounts Overview")