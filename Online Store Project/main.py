# main.py
import unittest
import time

from element import WebDriverSetup
from page import LoginPage, ProductsPage, CartPage, CheckoutPage

class SauceDemoTests(unittest.TestCase):

    def setUp(self):
        # Initialize WebDriver
        self.driver = WebDriverSetup().get_driver()
        self.driver.get('https://www.saucedemo.com/')

    def login(self):
        """Helper method for logging in."""
        login_page = LoginPage(self.driver)
        login_page.login('standard_user', 'secret_sauce')

    def enter_shipping_information(self):
        """Helper method for entering shipping information."""
        checkout_page = CheckoutPage(self.driver)
        checkout_page.enter_shipping_information('John', 'Doe', '12345')

    def test_login_success(self):
        # Test successful login using the helper method
        self.login()
        # Verify that login was successful by checking the URL
        self.assertIn("inventory", self.driver.current_url)

    def test_invalid_login(self):
        # Test invalid login attempt
        login_page = LoginPage(self.driver)
        login_page.login('invalid_user', 'invalid_password')
        error_message = login_page.get_error_message()
        self.assertIn("Username and password do not match any user in this service", error_message)

    def test_login_add_item_checkout(self):
        # Use the helper method to log in
        self.login()

        # Add an item to the cart
        products_page = ProductsPage(self.driver)
        products_page.add_item_to_cart()
        products_page.go_to_cart()

        # Proceed to checkout
        cart_page = CartPage(self.driver)
        cart_page.proceed_to_checkout()

        # Use the helper method to enter shipping details
        self.enter_shipping_information()

        # Finish checkout
        checkout_page = CheckoutPage(self.driver)
        checkout_page.finish_checkout()

        # Verify that the checkout was successful
        success_message = checkout_page.get_checkout_complete_message()
        self.assertIn("Thank you for your order!", success_message)
        time.sleep(5)  # Add a wait to observe the result

    def test_cancel_checkout_and_verify_cart(self):
        # Use the helper method to log in
        self.login()

        # Add multiple items to the cart
        products_page = ProductsPage(self.driver)
        products_page.add_item_to_cart(item_index=0)  # Add first item
        products_page.add_item_to_cart(item_index=1)  # Add second item
        products_page.go_to_cart()

        # Verify that items are added to the cart before proceeding
        cart_page = CartPage(self.driver)
        cart_items_before_checkout = cart_page.get_cart_items()
        self.assertEqual(len(cart_items_before_checkout), 2)  # Verify 2 items are added

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Use the helper method to enter shipping details
        self.enter_shipping_information()

        # Cancel the checkout process on the last step (before finishing)
        checkout_page = CheckoutPage(self.driver)
        checkout_page.cancel_checkout()

        # Navigate explicitly to the cart page after canceling checkout
        products_page.go_to_cart()

        # Verify that the cart still contains the items
        cart_items_after_cancellation = cart_page.get_cart_items()
        self.assertEqual(len(cart_items_after_cancellation), 2)  # We expect 2 items in the cart
        time.sleep(5)  # Add a wait to observe the result
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
