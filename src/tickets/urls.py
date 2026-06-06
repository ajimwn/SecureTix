from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    
    # Authentication pages
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Secure Booking & Profile pages (These were missing!)
    path('profile/', views.profile, name='profile'),
    path('concert/<uuid:concert_id>/', views.concert_detail, name='concert_detail'),
    path('book/<uuid:concert_id>/', views.book_ticket, name='book_ticket'),
    path('receipt/<uuid:booking_id>/', views.receipt, name='receipt'),
]