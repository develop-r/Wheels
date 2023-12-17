from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_name = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    miles_driven = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_photo = models.ImageField(upload_to='car_photos/', blank=True, null=True)

    def __str__(self):
        return self.car_name

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Booking {self.booking_id}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)  

    def __str__(self):
        return f"Feedback by {self.user.username}"