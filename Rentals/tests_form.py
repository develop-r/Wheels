"""
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

class LoginTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_login_form(self):
        # Open the login page
        self.selenium.get(self.live_server_url + '/login/')
        
        # Find form elements by their name attributes and input data
        username_input = self.selenium.find_element(by='name', value='username')
        password_input = self.selenium.find_element(by='name', value='password')


        username_input.send_keys("admin")
        password_input.send_keys("admin")

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Add assertions to check if the login was successful or if you see an error message
        # For example, you can check if the user is redirected to the home page
        time.sleep(1)  # Add a small delay to allow the page to load
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/login/')
    

    def test_signup_form(self):
        # Open the signup page
        self.selenium.get(self.live_server_url + '/signup/')
        
        # Find form elements by their name attributes and input data
        username_input = self.selenium.find_element(by='name', value='username')
        password1_input = self.selenium.find_element(by='name', value='password1')
        password2_input = self.selenium.find_element(by='name', value='password2')

        
        username_input.send_keys("testuser")
        password1_input.send_keys("testpassword")
        password2_input.send_keys("testpassword")

        # Submit the form
        password2_input.send_keys(Keys.RETURN)

        # Add assertions to check if the signup was successful or if you see an error message
        # For example, you can check if the user is redirected to the home page
        time.sleep(1)  # Add a small delay to allow the page to load
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/signup/')
        """
