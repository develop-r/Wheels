from django.test import TestCase
from django.contrib.auth.models import User
from .models import Car, Booking

class CarModelTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            car_name="Test Car",
            car_model="Model XYZ",
            car_year=2022,
            city="Test City",
            pickup_location="Test Location",
            pickup_latitude=12.345678,
            pickup_longitude=45.678901,
            miles_driven=1000.0,
            cost_per_day=50.0,
            car_photo=None  # You can provide a file path here if needed
        )

    def test_car_model(self):
        self.assertEqual(str(self.car), "Test Car")

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.car = Car.objects.create(
            car_name="Test Car",
            car_model="Model XYZ",
            car_year=2022,
            city="Test City",
            pickup_location="Test Location",
            pickup_latitude=12.345678,
            pickup_longitude=45.678901,
            miles_driven=1000.0,
            cost_per_day=50.0,
            car_photo=None
        )
        self.booking = Booking.objects.create(
            car=self.car,
            user=self.user,
            booking_start_date="2023-11-01",
            booking_end_date="2023-11-05",
            total_amount=250.0
        )

    def test_booking_model(self):
        self.assertEqual(str(self.booking), "Booking 1")
