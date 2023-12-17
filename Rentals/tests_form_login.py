"""
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        # Set up a user for the tests
        cls.test_user = User.objects.create_user('myuser', 'myuser@example.com', 'mypassword')

    @classmethod
    def tearDownClass(cls):
        # Clean up after test
        cls.test_user.delete()
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f'{self.live_server_url}/login/')  # Adjust the URL to your login route
        
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        submit_button = self.selenium.find_element(By.XPATH, '//button[@type="submit"]')
        
        username_input.send_keys('myuser')
        password_input.send_keys('mypassword')
        submit_button.submit()
        
        WebDriverWait(self.selenium, 10).until(
            EC.url_to_be(self.live_server_url + '/')
        )


# python manage.py test Rentals.tests_form_login.LoginSeleniumTests
"""