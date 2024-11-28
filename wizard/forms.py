from django import forms
from . models import Booking
from .models import Event, Comment
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class DateInput(forms.DateInput):
    input_type='date'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        model = Booking
        fields = ['cus_name', 'cus_ph', 'email', 'cus_email', 'details', 'booking_date']
        widgets = {
            'booking_date': DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'cus_name': "Customer Name:",
            'cus_ph': "Customer Phone:",
            'email': "Email Address:",
            'cus_email': "email address",
            'details': "Details:",
            'booking_date': "Booking Date:",
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        # Ensure the booking date is not in the past
        if booking_date < now().date():
            raise ValidationError("Booking date cannot be in the past.")
        return booking_date