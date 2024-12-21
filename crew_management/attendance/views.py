# attendance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance, Overtime
from .forms import AttendanceForm, OvertimeForm
import json




@login_required
def clock_in(request):
    if request.method == 'POST':
        date = timezone.now().date()
        # Ensure clock_in is set when creating a new record
        attendance, created = Attendance.objects.get_or_create(
            user=request.user,
            date=date,
            defaults={'clock_in': timezone.now()}  # Ensure clock_in is set to current time
        )
        
        if created:
            messages.success(request, 'You have successfully clocked in.')
        else:
            messages.warning(request, 'You have already clocked in today.')
    return redirect('crew_dashboard')


@login_required
def clock_out(request):
    date = timezone.now().date()
    try:
        attendance = Attendance.objects.get(user=request.user, date=date)
        if not attendance.clock_out:
            attendance.clock_out = timezone.now()
            attendance.save()
            messages.success(request, 'You have successfully clocked out.')
        else:
            messages.warning(request, 'You have already clocked out today.')
    except Attendance.DoesNotExist:
        messages.error(request, 'You need to clock in first.')
    return redirect('crew_dashboard')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Attendance

@login_required
def attendance_list(request):
    user = request.user
    today = timezone.now().date()
    
    # Get or create today's attendance
    attendance, created = Attendance.objects.get_or_create(
        user=user,
        date=today,
        defaults={'clock_in': None, 'clock_out': None}
    )
    
    # Handle clock in/out actions
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clock_in' and not attendance.clock_in:
            attendance.clock_in = timezone.now()
            attendance.save()
            messages.success(request, 'Clocked in successfully.')
        elif action == 'clock_out' and attendance.clock_in and not attendance.clock_out:
            attendance.clock_out = timezone.now()
            attendance.save()
            messages.success(request, 'Clocked out successfully.')
        return redirect('attendance_list')
    
    # Get recent attendance records
    recent_attendance = Attendance.objects.filter(user=user).order_by('-date')[:7]  # Last 7 days
    
    context = {
        'attendance': attendance,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'attendance/attendance_list.html', context)

@login_required
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    overtime_form = OvertimeForm()
    
    if request.method == 'POST':
        overtime_form = OvertimeForm(request.POST)
        if overtime_form.is_valid():
            overtime = overtime_form.save(commit=False)
            overtime.attendance = attendance
            overtime.save()
            messages.success(request, 'Overtime request submitted successfully.')
            return redirect('attendance_detail', pk=pk)
    
    return render(request, 'attendance/attendance_detail.html', {
        'attendance': attendance,
        'overtime_form': overtime_form
    })

@login_required
def time_tracking(request):
    date = timezone.now().date()
    try:
        attendance = Attendance.objects.get(user=request.user, date=date)
        context = {
            'clocked_in': attendance.clock_in is not None,
            'shift_start': attendance.clock_in.strftime('%I:%M %p') if attendance.clock_in else 'N/A',
            'hours_worked': calculate_hours_worked(attendance),
        }
    except Attendance.DoesNotExist:
        context = {
            'clocked_in': False,
            'shift_start': 'N/A',
            'hours_worked': '0h 0m',
        }
    return render(request, 'attendance/attendance_list.html', context)

def calculate_hours_worked(attendance):
    if attendance.clock_in:
        end_time = attendance.clock_out or timezone.now()
        duration = end_time - attendance.clock_in
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes = remainder // 60
        return f"{int(hours)}h {int(minutes)}m"
    return '0h 0m'

@login_required
def clock_action(request):
    if request.method == 'POST':
        date = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(user=request.user, date=date)
        
        if not attendance.clock_in:
            attendance.clock_in = timezone.now()
        elif not attendance.clock_out:
            attendance.clock_out = timezone.now()
        
        attendance.save()
    
    return redirect('time_tracking')


@login_required
def clock_in_out(request):
    if request.method == 'POST':
        date = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(user=request.user, date=date)

        if attendance.clock_in is None:  # If the user is clocking in
            attendance.clock_in = timezone.now()
        else:  # If the user is clocking out
            attendance.clock_out = timezone.now()

        attendance.save()
        return redirect('crew_dashboard')  # Redirect to the dashboard or appropriate page

    return redirect('crew_dashboard')  # Fallback redirect



