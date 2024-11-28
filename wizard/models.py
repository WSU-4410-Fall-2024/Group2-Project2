from django.db import models
from django.contrib.auth.models import User  # Import User model
from django.utils.timezone import now 
from django.core.exceptions import ValidationError

# Create your models here.
class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    image = models.ImageField(upload_to='events/', default='media/e1.jpg')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]

class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

from datetime import date
from django.core.exceptions import ValidationError

class Booking(models.Model):
    cus_name = models.CharField(max_length=55)
    cus_ph = models.CharField(max_length=12)
    email = models.EmailField()
    cus_email = models.EmailField()
    details = models.TextField()  # New field
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)

    def clean(self):
        # Ensure the booking_date is not None and is in the future
        if self.booking_date is None:
            raise ValidationError("Booking date cannot be empty.")
        if self.booking_date < date.today():
            raise ValidationError("Booking date must be today or a future date.")

    def __str__(self):
        return f"{self.cus_name} - {self.booking_date}"


