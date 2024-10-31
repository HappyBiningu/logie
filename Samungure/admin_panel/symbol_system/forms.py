# symbol_system/forms.py

from django import forms
from .models import Job, Driver, Vehicle, Customer, Parcel

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'assigned_to', 'vehicle']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'is_available'] 

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'model', 'license_expiry_date', 'last_maintenance_date']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'license_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
      
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_number', 'email']

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields =['tracking_number', 'weight', 'customer', 'job', 'destination', 'status']  # Include 'job' if not already there
        widgets = {
            'job': forms.Select()  # Add a dropdown for selecting the job
        }
        
class VehicleMaintenanceForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'model', 'license_expiry_date', 'last_maintenance_date']
        widgets = {
            'license_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'last_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }