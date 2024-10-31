# symbol_system/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Driver, Vehicle, Customer, Parcel
from .forms import JobForm, DriverForm, VehicleForm, CustomerForm, ParcelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# symbol_system/views.py

from django.shortcuts import render, redirect, get_object_or_404  # Ensure get_object_or_404 is imported
from django.contrib.auth.decorators import login_required
from .models import Job, Driver, Vehicle, Customer, Parcel
from .forms import JobForm, DriverForm, VehicleForm, CustomerForm, ParcelForm, VehicleMaintenanceForm  # Import VehicleMaintenanceForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count


# Login view
def login_view(request):
    if request.user.is_authenticated:  # If user is already logged in, redirect to dashboard
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'symbol_system/login.html')  # Render login template

# Signup view
def signup_view(request):
    if request.user.is_authenticated:  # If user is already logged in, redirect to dashboard
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Redirect to login after successful signup
        except:
            messages.error(request, 'Failed to create account. Username might be taken.')
    return render(request, 'symbol_system/signup.html')  # Render signup template

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'symbol_system/logout.html')  # Use the logout template



@login_required
def dashboard(request):
    # Job Status Data for Chart.js
    pending_jobs = Job.objects.filter(status='pending').count()
    in_progress_jobs = Job.objects.filter(status='in_progress').count()
    completed_jobs = Job.objects.filter(status='completed').count()
    job_status_data = [pending_jobs, in_progress_jobs, completed_jobs]

    # Driver Availability Data for Chart.js
    drivers = Driver.objects.all()
    driver_labels = [driver.name for driver in drivers]
    driver_availability_data = [1 if driver.is_available else 0 for driver in drivers]

    # Parcel Delivered Data
    parcels_delivered = Parcel.objects.filter(status='delivered').count()
    pending_parcels = Parcel.objects.filter(status='pending')

    # Vehicle Data
    vehicle_data = Vehicle.objects.values('model').annotate(count=Count('id'))  # Group by vehicle model and count
    vehicle_labels = [vehicle['model'] for vehicle in vehicle_data]
    vehicle_counts = [vehicle['count'] for vehicle in vehicle_data]

    # Maintenance and License Expiry Data for Vehicles
    vehicles = Vehicle.objects.all()
    vehicles_license_expiring = [vehicle for vehicle in vehicles if vehicle.license_expiry_soon()]
    vehicles_due_for_maintenance = [vehicle for vehicle in vehicles if vehicle.maintenance_due()]

    # Summary Data
    total_jobs = Job.objects.all().count()
    active_drivers = Driver.objects.filter(is_available=True).count()

    context = {
        'jobs': Job.objects.all(),
        'job_status_data': job_status_data,
        'driver_labels': driver_labels,
        'driver_availability_data': driver_availability_data,
        'total_jobs': total_jobs,
        'active_drivers': active_drivers,
        'parcels_delivered': parcels_delivered,
        'vehicle_labels': vehicle_labels,
        'vehicle_counts': vehicle_counts,
        'pending_parcels': pending_parcels,
        'vehicles_license_expiring': vehicles_license_expiring,
        'vehicles_due_for_maintenance': vehicles_due_for_maintenance,
    }
    return render(request, 'symbol_system/dashboard.html', context)




@login_required
def add_job(request):
    drivers = Driver.objects.filter(is_available=True)  # Get available drivers
    vehicles = Vehicle.objects.all()  # Get all vehicles
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobForm()

    context = {
        'form': form,
        'drivers': drivers,
        'vehicles': vehicles,
    }
    return render(request, 'symbol_system/add_job.html', context)


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DriverForm()
    return render(request, 'symbol_system/add_driver.html', {'form': form})


@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'symbol_system/add_vehicle.html', {'form': form})

@login_required
def add_parcel(request):
    jobs = Job.objects.all() 
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        job_id = request.GET.get('job_id')
        if job_id:
            job = Job.objects.get(id=job_id)
            form = ParcelForm(initial={'job': job})  # Pre-fill the job field
        else:
            form = ParcelForm()
    return render(request, 'symbol_system/add_parcel.html', {'form': form, 'jobs' : jobs})






@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'symbol_system/edit_job.html', {'form': form})


@login_required
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'symbol_system/edit_driver.html', {'form': form})

@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'symbol_system/edit_vehicle.html', {'form': form})

@login_required
def edit_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    if request.method == 'POST':
        form = ParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ParcelForm(instance=parcel)
    return render(request, 'symbol_system/edit_parcel.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('dashboard')

@login_required
def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.delete()
    return redirect('dashboard')

@login_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.delete()
    return redirect('dashboard')

@login_required
def delete_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    parcel.delete()
    return redirect('dashboard')




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt  # Disable CSRF token check for simplicity (though it's better to secure this in production)

@login_required
def mark_delivered(request, parcel_id):
    if request.method == 'POST':
        try:
            parcel = Parcel.objects.get(id=parcel_id)
            parcel.status = 'delivered'
            parcel.save()

            # Check if the parcel is linked to a job
            if parcel.job:  # Ensure the parcel has an associated job
                job = parcel.job
                print(f"Checking job {job.id} for completion status.")

                # Get the statuses of all parcels linked to this job
                parcel_statuses = [p.status for p in job.parcels.all()]
                
                if all(status == 'delivered' for status in parcel_statuses):
                    job.status = 'completed'  # Mark job as completed
                    print(f"Job {job.id} marked as completed.")
                elif any(status == 'delivered' for status in parcel_statuses):
                    job.status = 'in_progress'  # Mark job as in progress
                    print(f"Job {job.id} marked as in progress.")
                else:
                    job.status = 'pending'  # Mark job as pending
                    print(f"Job {job.id} marked as pending.")

                job.save()

            return JsonResponse({'success': True})
        except Parcel.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Parcel not found.'})




from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=Parcel)
def update_job_status(sender, instance, created, **kwargs):
    # If the parcel is delivered and linked to a job, check if all parcels are delivered
    if instance.job:
        job = instance.job
        # If all parcels for this job are delivered, mark the job as completed
        if all(parcel.status == 'delivered' for parcel in job.parcels.all()):
            job.status = 'completed'
        else:
            # If there are still pending parcels, the job is in progress
            job.status = 'in_progress'
        job.save()

@login_required
def update_vehicle_maintenance(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleMaintenanceForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleMaintenanceForm(instance=vehicle)
    
    context = {
        'form': form,
        'vehicle': vehicle,
    }
    return render(request, 'symbol_system/update_vehicle_maintenance.html', context)






def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'symbol_system/vehicle_list.html', {'vehicles': vehicles})

def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleMaintenanceForm()
    return render(request, 'symbol_system/vehicle_form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleMaintenanceForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehicleMaintenanceForm(instance=vehicle)
    return render(request, 'symbol_system/vehicle_form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('dashboard')
    return render(request, 'symbol_system/vehicle_confirm_delete.html', {'vehicle': vehicle})






from datetime import timedelta, date

def get_vehicle_status(vehicle):
    today = date.today()
    if vehicle.license_expiry_date < today:
        vehicle.is_license_expired = True
        vehicle.is_license_near_expiry = False
    elif vehicle.license_expiry_date <= today + timedelta(days=30):
        vehicle.is_license_expired = False
        vehicle.is_license_near_expiry = True
    else:
        vehicle.is_license_expired = False
        vehicle.is_license_near_expiry = False

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        get_vehicle_status(vehicle)
    context = {'vehicles_license_expiring': vehicles}
    return render(request, 'symbol_system/dashboard.html', context)


def get_maintenance_status(vehicle):
    today = date.today()
    # Assume maintenance due every 6 months (or define your interval)
    maintenance_interval = timedelta(days=18) 
    next_maintenance_due = vehicle.last_maintenance_date + maintenance_interval
    
    if next_maintenance_due < today:
        vehicle.is_maintenance_overdue = True
        vehicle.is_maintenance_due_soon = False
    elif next_maintenance_due <= today + timedelta(days=3):
        vehicle.is_maintenance_overdue = False
        vehicle.is_maintenance_due_soon = True
    else:
        vehicle.is_maintenance_overdue = False
        vehicle.is_maintenance_due_soon = False

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        get_maintenance_status(vehicle)
    context = {'vehicles_due_for_maintenance': vehicles}
    return render(request, 'symbol_system/dashboard.html', context)