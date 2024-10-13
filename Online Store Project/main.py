import unittest
import time
from element import WebDriverSetup
from page import LoginPage, ProductsPage, CartPage, CheckoutPage, MenuPage
from locators import LoginPageLocators, ProductsPageLocators  # Import ProductsPageLocators

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

    def test_sort_products_by_price(self):
        # Use the helper method to log in
        self.login()

        # Sort products by "Price (low to high)"
        products_page = ProductsPage(self.driver)
        products_page.sort_products("Price (low to high)")

        # Get the list of product prices and verify ascending order
        product_prices_low_to_high = products_page.get_product_prices()
        self.assertEqual(product_prices_low_to_high, sorted(product_prices_low_to_high))

        # Sort products by "Price (high to low)"
        products_page.sort_products("Price (high to low)")

        # Get the list of product prices and verify descending order
        product_prices_high_to_low = products_page.get_product_prices()
        self.assertEqual(product_prices_high_to_low, sorted(product_prices_high_to_low, reverse=True))

    def test_sort_products_by_name(self):
        # Use the helper method to log in
        self.login()

        # Sort products by "Name (A to Z)"
        products_page = ProductsPage(self.driver)
        products_page.sort_products("Name (A to Z)")

        # Get the list of product names and verify ascending order
        product_names_a_to_z = products_page.get_product_names()
        self.assertEqual(product_names_a_to_z, sorted(product_names_a_to_z))

        # Sort products by "Name (Z to A)"
        products_page.sort_products("Name (Z to A)")

        # Get the list of product names and verify descending order
        product_names_z_to_a = products_page.get_product_names()
        self.assertEqual(product_names_z_to_a, sorted(product_names_z_to_a, reverse=True))


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

    def test_sql_injection_in_username(self):
        # Use SQL injection string in the username field with a valid password
        sql_injection_string = "' OR '1'='1"
        login_page = LoginPage(self.driver)
        login_page.login(sql_injection_string, "secret_sauce")  # Use valid password

        # Verify that login attempt fails
        error_message = login_page.get_error_message()
        self.assertIn("Username and password do not match any user in this service", error_message)


    def test_sql_injection_in_password(self):
        # Use SQL injection string in the password field with a valid username
        sql_injection_string = "' OR '1'='1"
        login_page = LoginPage(self.driver)
        login_page.login("standard_user", sql_injection_string)  # Use valid username

        # Verify that login attempt fails
        error_message = login_page.get_error_message()
        self.assertIn("Username and password do not match any user in this service", error_message)

        time.sleep(5)  # Add a wait to observe the result

    def test_network_disconnection_during_checkout(self):
        # Step 1: Log in to the application
        self.login()

        # Step 2: Add item to the cart
        products_page = ProductsPage(self.driver)
        products_page.add_item_to_cart()
        products_page.go_to_cart()

        # Step 3: Proceed to checkout
        cart_page = CartPage(self.driver)
        cart_page.proceed_to_checkout()

        # Step 4: Enter shipping details
        self.enter_shipping_information()

        # Step 5: Simulate network disconnection using Chrome DevTools Protocol
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": True,
            "latency": 0,
            "downloadThroughput": 0,
            "uploadThroughput": 0
        })

        # Step 6: Try to finish checkout while the network is disconnected using the checkout_page object
        checkout_page = CheckoutPage(self.driver)
        try:
            checkout_page.finish_checkout()  # Attempt to finish checkout while offline
        except:
            print("Checkout failed due to network disconnection as expected.")

        # Step 7: Wait to observe any changes (e.g., an error message due to no connection)
        time.sleep(5)

        # Step 8: Reconnect the network
        self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 50,
            "downloadThroughput": 5000000,
            "uploadThroughput": 3000000
        })

        # Step 9: Retry finishing checkout after reconnection
        time.sleep(2)  # Wait for network stabilization
        checkout_page.finish_checkout()  # Attempt to finish the checkout again

        # Verify that the checkout was successful
        success_message = checkout_page.get_checkout_complete_message()
        self.assertIn("Thank you for your order!", success_message)
        time.sleep(2)  # Add a wait to observe the successful checkout result

    def test_end_to_end_scenario(self):
        # Step 1: Log in to the application
        self.login()

        # Step 2: Sort products by "Name (A to Z)"
        products_page = ProductsPage(self.driver)
        products_page.sort_products("Name (A to Z)")
        time.sleep(2)  # Wait to observe sorting result

        # Step 3: Add three items to the cart
        available_items = self.driver.find_elements(*ProductsPageLocators.ADD_TO_CART_BUTTON)
        item_indices_to_add = min(3, len(available_items))  # Determine how many items can be added

        for index in range(item_indices_to_add):
            products_page.add_item_to_cart(item_index=index)  # Add items based on available count

        products_page.go_to_cart()

        # Step 4: Proceed to checkout
        cart_page = CartPage(self.driver)
        cart_page.proceed_to_checkout()

        # Step 5: Enter shipping details and proceed to the final checkout page
        self.enter_shipping_information()

        # Step 6: Cancel the checkout process on the last page
        checkout_page = CheckoutPage(self.driver)
        checkout_page.cancel_checkout()

        # Step 7: Navigate back to the products page to add one more item to the cart
        self.driver.get('https://www.saucedemo.com/inventory.html')  # Navigate back to the products page
        time.sleep(2)  # Wait for the page to load

        # Update the list of available items after navigating back
        available_items = self.driver.find_elements(*ProductsPageLocators.ADD_TO_CART_BUTTON)

        if len(available_items) > item_indices_to_add:
            products_page.add_item_to_cart(item_index=item_indices_to_add)  # Add another item if available
        else:
            print("No additional items are available to add.")

        products_page.go_to_cart()

        # Step 8: Proceed to checkout again
        cart_page.proceed_to_checkout()
        self.enter_shipping_information()

        # Step 9: Finish checkout process
        checkout_page.finish_checkout()

        # Verify that the checkout was successful
        success_message = checkout_page.get_checkout_complete_message()
        self.assertIn("Thank you for your order!", success_message)
        time.sleep(2)  # Add a wait to observe the successful checkout result

        # Step 10: Log out
        menu_page = MenuPage(self.driver)
        menu_page.logout()

        # Verify that user is redirected to the login page after logout
        self.assertIn("https://www.saucedemo.com/", self.driver.current_url)
        self.assertTrue(self.driver.find_element(*LoginPageLocators.USERNAME_INPUT).is_displayed())

        time.sleep(2)  # Add a wait to observe the result after logout

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
