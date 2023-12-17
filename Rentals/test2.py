from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
from .models import Car, Booking, Feedback

class YourViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test car
        self.car = Car.objects.create(
            car_name='Test Car',
            car_model='Test Model',
            car_year=2022,
            city='Test City',
            pickup_location='Test Location',
            pickup_latitude=12.345678,
            pickup_longitude=45.678901,
            miles_driven=1000.0,
            cost_per_day=50.0,
        )

        # Create a test booking
        self.booking = Booking.objects.create(
            car=self.car,
            user=self.user,
            booking_start_date='2022-11-01',
            booking_end_date='2022-11-05',
            total_amount=250.0,
        )

        # Create a test feedback
        self.feedback = Feedback.objects.create(
            user=self.user,
            rating=5,
            feedback='This is a test feedback.',
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_book_view(self):
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)

    def test_confirmation_view(self):
        response = self.client.get(reverse('confirmation'))
        self.assertEqual(response.status_code, 200)

    def test_aboutus_view(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_contactus_view(self):
        response = self.client.get(reverse('contactus'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to home after logout

    def test_feedback_view(self):
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)

    def test_bookings_view(self):
        # Login the test user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_view(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)

    # You can add more test cases for your views as needed
