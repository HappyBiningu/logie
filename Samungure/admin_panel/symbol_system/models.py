from django.db import models
from datetime import timedelta, date
from django.utils import timezone

class Driver(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=255)
    license_expiry_date = models.DateField(default=timezone.now)   # New field for license expiry
    last_maintenance_date = models.DateField(default=timezone.now)   # New field for last maintenance date

    def __str__(self):
        return self.license_plate

    def license_expiry_soon(self):
        """Returns True if the license expires in the next 3 months"""
        today = date.today()
        return today + timedelta(days=90) >= self.license_expiry_date

    def maintenance_due(self):
        """Returns True if more than 2 months have passed since last maintenance"""
        today = date.today()
        return today >= self.last_maintenance_date + timedelta(days=60)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    ]

    tracking_number = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    job = models.ForeignKey('Job', related_name='parcels', on_delete=models.CASCADE, null=True, blank=True)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('delivered', 'Delivered')])

    def __str__(self):
        return self.tracking_number

    def mark_as_delivered(self):
        self.status = 'delivered'
        self.save()
        if self.job:
            self.job.status = 'completed'
            self.job.save()


class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return self.title
