from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date, timedelta
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Car, Booking, Feedback
from django.db.models import F, Func, ExpressionWrapper, DecimalField, Value, Q
from math import radians, sin, cos, sqrt, atan2
import math
from django.http import JsonResponse
from django.core import serializers
from django.utils.dateparse import parse_date

def get_blocked_dates(car_id):
    # Get today's date
    today = date.today()

    # Calculate the end date as today + 3 months
    three_months_from_now = today + timedelta(days=90)

    # Query the Booking model to get booked dates for the specified car within the date range
    bookings = Booking.objects.filter(
        Q(booking_start_date__gte=today, booking_start_date__lte=three_months_from_now, car_id=car_id) |
        Q(booking_end_date__gte=today, booking_end_date__lte=three_months_from_now, car_id=car_id) |
        Q(booking_start_date__lte=today, booking_end_date__gte=three_months_from_now, car_id=car_id)
    )

    # Create a list of blocked dates in yyyy-mm-dd format
    blocked_dates = set()
    for booking in bookings:
        current_date = booking.booking_start_date
        while current_date <= booking.booking_end_date:
            blocked_dates.add(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

    return list(blocked_dates)


def get_cars_within_distance(user_lat, user_long, max_distance):
    # Earth radius in kilometers
    earth_radius_km = 6371

    # Convert user's latitude and longitude to radians
    user_lat_rad = math.radians(user_lat)
    user_long_rad = math.radians(user_long)

    # Calculate the maximum latitude and longitude differences
    max_lat_diff = max_distance / earth_radius_km
    max_long_diff = max_distance / (earth_radius_km * math.cos(user_lat_rad))

    # Calculate the minimum and maximum latitude and longitude values
    min_lat = user_lat_rad - max_lat_diff
    max_lat = user_lat_rad + max_lat_diff
    min_long = user_long_rad - max_long_diff
    max_long = user_long_rad + max_long_diff

    # Convert the minimum and maximum latitude and longitude values back to degrees
    min_lat_deg = math.degrees(min_lat)
    max_lat_deg = math.degrees(max_lat)
    min_long_deg = math.degrees(min_long)
    max_long_deg = math.degrees(max_long)

    # Query the database for cars within the specified latitude and longitude range
    cars_within_distance = Car.objects.filter(
        pickup_latitude__gte=min_lat_deg,
        pickup_latitude__lte=max_lat_deg,
        pickup_longitude__gte=min_long_deg,
        pickup_longitude__lte=max_long_deg
    )

    return cars_within_distance

def home(request):
    cars = Car.objects.all()
    # try:
    filter_type = request.GET.get('filter-type')
    if filter_type == 'city':
        city = request.GET.get('city')
        cars = Car.objects.filter(city__iexact=city)
    elif filter_type == 'location':
        user_lat = float(request.GET.get('user-lat'))
        user_long = float(request.GET.get('user-long'))
        max_distance = float(request.GET.get('max-distance'))
        if max_distance >= 22000:
            max_distance = 22000
        cars = get_cars_within_distance(user_lat, user_long, max_distance)
    else:
        cars = Car.objects.all()
    # except:
    #     print("error")

    return render(request, 'home.html', {'cars': cars})

def signup(request):
    return render(request, 'signup.html')

def book(request):
    if request.method == 'POST':
        # try:
        # Extract data from the JSON object
        raw_body = request.body
        content_type = request.content_type
        raw_body_decoded = raw_body.decode('utf-8')
        data = json.loads(raw_body_decoded)
        print(data)
        car_id = data.get('car_id')
        user = request.user  # Get the currently authenticated user
        booking_start_date = data.get('booking_start_date')
        booking_end_date = data.get('booking_end_date')
        total_amount = data.get('total_amount')

        # Create a Booking object
        booking = Booking.objects.create(
            car_id=car_id,
            user=user,
            booking_start_date=booking_start_date,
            booking_end_date=booking_end_date,
            total_amount=total_amount
        )
        response_data = {'message': 'Booking successful'}
        return JsonResponse(response_data)
        # except:
        #     # Handle other HTTP methods if needed
        #     return JsonResponse({'message': 'Invalid request method'}, status=400)
    try:
        car_id = request.GET.get('car_id')
        car = Car.objects.filter(car_id=car_id)
        car_json = serializers.serialize('json', car)
        blocked_dates = get_blocked_dates(car_id)
        # blocked_dates = [
        #     date(2023, 11, 15),
        #     date(2023, 11, 16),
        #     date(2023, 11, 17),
        #     # Add more blocked dates as needed
        # ]
        blocked_dates_str = [str(d) for d in blocked_dates]
        blocked_dates_json = json.dumps(blocked_dates_str)
        context = {'blocked_dates': blocked_dates_json, 'car': car_json}
        return render(request, 'book.html', context)
    except:
        return render(request, 'home.html')

def confirmation(request):
    return render(request, 'confirmation.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('home')  # Redirect to your home or dashboard page
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your home or dashboard page after successful login
        else:
            # Handle invalid login credentials, e.g., display an error message
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def feedback(request):
    if request.method == 'POST':
        rating = request.POST['rating']
        feedback_text = request.POST['feedback']
        user = request.user
        feedback_entry = Feedback(user=user, rating=rating, feedback=feedback_text)

        # Save the feedback entry to the database
        feedback_entry.save()

        # Redirect to a success page or another appropriate view
        return redirect('home')

    return render(request, 'feedback.html')


def bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user = user).select_related('car')  
    return render(request, 'bookings.html', {'bookings': bookings})

def forgot_password(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            # Handle the case when the user with the provided username does not exist
            messages.error(request, f'User with username {username} does not exist.')

    return render(request, 'forgot_password.html')