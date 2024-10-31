# symbol_system/urls.py

from django.urls import path
from . import views
from .views import mark_delivered, vehicle_list, vehicle_create, vehicle_update, vehicle_delete

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),  # URL for login page
    path('signup/', views.signup_view, name='signup'),  # URL for signup page
    path('accounts/logout/', views.logout_view, name='logout'),  # URL for logout
    path('dashboard/add-job/', views.add_job, name='add_job'),
    path('add-driver/', views.add_driver, name='add_driver'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('add-parcel/', views.add_parcel, name='add_parcel'),
    path('vehicles', vehicle_list, name='vehicle_list'),
    path('vehicle/new/', vehicle_create, name='vehicle_create'),
    path('vehicle/<int:pk>/edit/', vehicle_update, name='vehicle_update'),
    path('vehicle/<int:pk>/delete/', vehicle_delete, name='vehicle_delete'),
    #path('vehicle_maintenance/', views.vehicle_maintenance, name='vehicle_maintenance'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('edit-driver/<int:driver_id>/', views.edit_driver, name='edit_driver'),
    path('edit-vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('edit-parcel/<int:parcel_id>/', views.edit_parcel, name='edit_parcel'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('delete-driver/<int:driver_id>/', views.delete_driver, name='delete_driver'),
    path('delete-vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('delete-parcel/<int:parcel_id>/', views.delete_parcel, name='delete_parcel'),
    path('mark-delivered/<int:parcel_id>/', mark_delivered, name='mark_delivered'),
    path('vehicle/<int:vehicle_id>/maintenance/', views.update_vehicle_maintenance, name='update_vehicle_maintenance'),
]
