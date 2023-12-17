"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SignupSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_signup(self):
        # Open the signup page
        self.selenium.get(f'{self.live_server_url}/signup/')  # Adjust to your actual signup URL

        # Fill out the signup form
        username_input = self.selenium.find_element(By.NAME, 'username')
        first_name_input = self.selenium.find_element(By.NAME, 'first_name')
        last_name_input = self.selenium.find_element(By.NAME, 'last_name')
        email_input = self.selenium.find_element(By.NAME, 'email')
        password1_input = self.selenium.find_element(By.NAME, 'password1')
        password2_input = self.selenium.find_element(By.NAME, 'password2')

        test_username = 'testuser'
        test_first_name = 'Test'
        test_last_name = 'User'
        test_email = 'testuser@example.com'
        test_password = 'TestPassword123'

        username_input.send_keys(test_username)
        first_name_input.send_keys(test_first_name)
        last_name_input.send_keys(test_last_name)
        email_input.send_keys(test_email)
        password1_input.send_keys(test_password)
        password2_input.send_keys(test_password)

        # Submit the form
        submit_button = self.selenium.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.submit()

        WebDriverWait(self.selenium, 10).until(
            EC.url_to_be(self.live_server_url + '/')
        )


# To run this test, use:
# python manage.py test Rentals.tests_form_signup.SignupSeleniumTests
"""