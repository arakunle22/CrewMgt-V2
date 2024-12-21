from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm
import json

@login_required
def leave_management(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('leave_management')
    else:
        form = LeaveRequestForm()
    
    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')
    leave_types = LeaveType.objects.all()
    
    leave_types_dict = {str(lt.id): {'name': lt.name, 'days_allowed': lt.days_allowed} for lt in leave_types}
    leave_types_json = json.dumps(leave_types_dict)
    
    context = {
        'form': form,
        'leave_requests': leave_requests,
        'leave_types_json': leave_types_json,
    }
    return render(request, 'leave/leave_management.html', context)

