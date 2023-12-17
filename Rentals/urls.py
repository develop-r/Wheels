from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup',views.signup, name='signup'),
    path('book',views.book, name='book'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feedback',views.feedback, name='feedback'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('contactus',views.contactus, name='contactus'),
    path('bookings',views.bookings, name='bookings'),
    path('forgot_password',views.forgot_password, name='forgot_password'),
]
