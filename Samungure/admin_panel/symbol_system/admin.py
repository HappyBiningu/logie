# symbol_system/admin.py

from django.contrib import admin
from .models import Job, Driver, Vehicle, Customer, Parcel

# Define custom admin actions (bulk deletion)
def mark_as_completed(modeladmin, request, queryset):
    queryset.update(status='completed')  # Assuming status is a field in Job model
mark_as_completed.short_description = 'Mark selected jobs as completed'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'assigned_to', 'vehicle', 'status', 'date_posted')
    search_fields = ('title', 'description')
    list_filter = ('assigned_to', 'vehicle')
    actions = [mark_as_completed]  # Bulk action to mark jobs as completed

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number')
    search_fields = ('name', 'license_number')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'model')
    search_fields = ('license_plate', 'model')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'email')
    search_fields = ('name', 'contact_number', 'email')

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'weight', 'destination', 'customer')
    search_fields = ('tracking_number', 'destination')
    list_filter = ('customer',)
