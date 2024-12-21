# user_management/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser
from attendance.models import Attendance
from scheduling.models import Shift, Schedule, Availability
from task_management.models import Task, TaskComment
from django.utils.timezone import now
from django.db.models import Q
from django.utils import timezone


def landing_page(request):
    return render(request, 'landing_page/landing_page.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please wait for admin approval before logging in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_management/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_approved:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    if user.role == 'manager':
                        return redirect('manager_dashboard')
                    elif user.role == 'admin':
                        return redirect('admin_approval')
                    else:
                        return redirect('crew_dashboard')
                else:
                    messages.warning(request, 'Your account is not yet approved. Please wait for admin approval.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'user_management/login.html', {'form': form})

def get_upcoming_shifts(user, date):
    return Schedule.objects.filter(user=user, date__gte=date).order_by('date')[:5]

@login_required
@user_passes_test(lambda u: u.role == 'crew_member')
def crew_dashboard(request):
    """
    Dashboard for crew members, including attendance information and tasks.
    """
    today = timezone.now().date()
    user = request.user

    # Get or create today's attendance
    attendance, created = Attendance.objects.get_or_create(
        user=user, 
        date=today,
        defaults={'clock_in': None, 'clock_out': None}
    )

    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'clock_in':
            if attendance.clock_in is None:
                attendance.clock_in = timezone.now()
                attendance.save()
                messages.success(request, "Clock-in successful!")
            else:
                messages.warning(request, "You have already clocked in today.")
                
        elif action == 'clock_out':
            if attendance.clock_in is None:
                messages.error(request, "You must clock in before clocking out.")
            elif attendance.clock_out is None:
                attendance.clock_out = timezone.now()
                attendance.save()
                messages.success(request, "Clock-out successful!")
            else:
                messages.warning(request, "You have already clocked out today.")
                
        return redirect('crew_dashboard')

    # Get tasks for the user
    tasks = Task.objects.filter(
        Q(assigned_to=user) | Q(created_by=user)
    ).order_by('due_date')[:5]  # Limit to 5 most recent tasks

    context = {
        'username': user.username,
        'attendance': attendance,
        'tasks': tasks,
        'shifts': get_upcoming_shifts(request.user, today),
    }
    return render(request, 'user_management/crew_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.role == 'manager')
def manager_dashboard(request):
    return render(request, 'user_management/manager_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    unapproved_users = CustomUser.objects.filter(is_approved=False)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_approved = True
        user.role = new_role
        user.save()
        messages.success(request, f'User {user.username} has been approved as {user.get_role_display()}.')
        return redirect('admin_approval')
    return render(request, 'user_management/admin_approval.html', {'unapproved_users': unapproved_users})

def user_logout(request):
    logout(request)
    return redirect('login')