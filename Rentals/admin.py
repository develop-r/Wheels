from django.contrib import admin
from .models import Car, Booking, Feedback

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'car_model', 'car_year', 'city', 'pickup_location', 'miles_driven', 'cost_per_day')
    list_filter = ('car_year', 'city')
    search_fields = ('car_name', 'car_model', 'pickup_location')
    list_editable = ('car_year', 'city', 'pickup_location', 'miles_driven', 'cost_per_day')

admin.site.register(Car, CarAdmin)



class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'car', 'user', 'booking_start_date', 'booking_end_date', 'total_amount')
    list_filter = ('car', 'user', 'booking_start_date', 'booking_end_date')
    search_fields = ('car__car_name', 'user__username', 'booking_start_date', 'booking_end_date')
    date_hierarchy = 'booking_start_date'

admin.site.register(Booking, BookingAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'feedback', 'date')
    list_filter = ('date',)
    search_fields = ('user__username', 'rating')
    list_per_page = 20  # Number of items to display per page in the admin list view

admin.site.register(Feedback, FeedbackAdmin)