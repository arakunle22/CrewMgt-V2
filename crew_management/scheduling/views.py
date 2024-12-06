from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Shift, Schedule, Availability
from .forms import AvailabilityForm

@login_required
def dashboard(request):
    today = timezone.now().date()
    context = {
        'active_view': 'dashboard',
        'profile': request.user,
        'attendance': get_today_attendance(request.user, today),
        'tasks': get_upcoming_tasks(request.user),
        'shifts': get_upcoming_shifts(request.user, today),
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clock_in':
            clock_in(request.user)
        elif action == 'clock_out':
            clock_out(request.user)
        return redirect('dashboard')
    
    return render(request, 'dashboard.html', context)

@login_required
def shift_schedule(request):
    today = timezone.now().date()
    upcoming_shifts = Schedule.objects.filter(user=request.user, date__gte=today).order_by('date')
    context = {
        'active_view': 'shift',
        'upcoming_shifts': upcoming_shifts,
    }
    return render(request, 'scheduling/shift_schedule.html', context)

@login_required
def availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            return redirect('availability')
    else:
        form = AvailabilityForm()
    
    availabilities = Availability.objects.filter(user=request.user).order_by('date')
    context = {
        'active_view': 'availability',
        'form': form,
        'availabilities': availabilities,
    }
    return render(request, 'scheduling/availability.html', context)

# Helper functions
def get_today_attendance(user, date):
    # Implement logic to get today's attendance
    pass

def get_upcoming_tasks(user):
    # Implement logic to get upcoming tasks
    pass

def get_upcoming_shifts(user, date):
    return Schedule.objects.filter(user=user, date__gte=date).order_by('date')[:5]

def clock_in(user):
    # Implement clock-in logic
    pass

def clock_out(user):
    # Implement clock-out logic
    pass