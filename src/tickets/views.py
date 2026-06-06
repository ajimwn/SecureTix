from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Concert, Booking, AuditLog
from .forms import CustomUserCreationForm, UserEditForm

def home(request: HttpRequest) -> HttpResponse:
    """Render the home page with a list of upcoming concerts."""
    concerts = Concert.objects.filter(date__gte=timezone.now()).order_by('date')
    context = {'concerts': concerts}
    return render(request, 'index.html', context)

def concert_detail(request: HttpRequest, concert_id: str) -> HttpResponse:
    """Displays details for a specific concert."""
    concert = get_object_or_404(Concert, id=concert_id)
    return render(request, 'concert_detail.html', {'concert': concert})

def register(request: HttpRequest) -> HttpResponse:
    """Secure user registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Account created securely! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def book_ticket(request: HttpRequest, concert_id: str) -> HttpResponse:
    """Securely creates a ticket booking and logs the action."""
    if request.method == 'POST':
        # Safely get the concert, or return a 404 error if tampered with
        concert = get_object_or_404(Concert, id=concert_id)
        
        if concert.is_past:
            messages.error(request, "This concert has already passed and cannot be booked.")
            return redirect('concert_detail', concert_id=concert.id)
            
        # Create the booking in the database
        Booking.objects.create(user=request.user, concert=concert)
        
        # SECURITY REQUIREMENT: Write to the Audit Log
        AuditLog.objects.create(
            user=request.user,
            action=f"Booked ticket for {concert.title}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f"Successfully booked your ticket for {concert.title}!")
        return redirect('profile')
        
    return redirect('home')

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Displays the user's purchased tickets and profile info."""
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'profile.html', {'bookings': bookings, 'form': form})

@login_required
def receipt(request: HttpRequest, booking_id: str) -> HttpResponse:
    """Displays the receipt for a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'receipt.html', {'booking': booking})