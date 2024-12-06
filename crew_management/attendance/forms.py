# attendance/forms.py
from django import forms
from .models import Attendance, Overtime

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'clock_in', 'clock_out']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'clock_in': forms.TimeInput(attrs={'type': 'time'}),
            'clock_out': forms.TimeInput(attrs={'type': 'time'}),
        }

class OvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = ['hours']