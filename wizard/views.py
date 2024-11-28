from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Comment, Booking
from .forms import BookingForm, EventForm, CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def is_superuser(user):
    return user.is_superuser

def events(request):
    events = Event.objects.all().order_by('-created_at')
    form = None

    if request.user.is_authenticated:
        form = EventForm()

    return render(request, 'events.html', {'events': events, 'form': form})

def events_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.owner = request.user
            event.save()
            return redirect('events')
    else:
        form = EventForm()

    events = Event.objects.all().order_by('-created_at')
    comment_form = CommentForm()  # Add this line to create an instance of CommentForm
    return render(request, 'events.html', {'form': form, 'events': events, 'comment_form': comment_form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect('events')
    return redirect('events')

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.owner or request.user.is_superuser:
        event.delete()
    return redirect('events')

@login_required
def add_comment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user  # Add this line
            comment.save()
    return redirect('events')

def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent = parent_comment
            reply.event = parent_comment.event
            reply.save()
    return redirect('events')

def reservations(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.full_clean()
                booking.save()
                send_mail(
                    'Reservation Confirmation',
                    f'Your reservation has been successfully booked!\nDetails:\nCustomer Name: {booking.cus_name}\nDate: {booking.booking_date}',
                    'northfieldhills@gmail.com',
                    [booking.cus_email],  # Assuming you have a cus_email field
                    fail_silently=False,
                )
                messages.success(request, "Your booking was successful!")
                return redirect('reservations')
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'reservations.html', {'form': form})

def cancel_reservation(request, reservation_id):
    reservation = Booking.objects.get(id=reservation_id, cus_name=request.user.username)
    if reservation:
        reservation.delete()
    return redirect('reservations')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        admin_email = 'northfieldhills@gmail.com'

        send_mail(
            f'Contact Inquiry from {name}',
            f'Message: {message}\nFrom: {email}',
            'northfieldhills@gmail.com',
            [admin_email],
            fail_silently=False,
        )
        messages.success(request, "Your inquiry has been sent successfully!")
    return render(request, 'contact.html')
