# attendance/models.py
from django.db import models
from user_management.models import CustomUser

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Overtime(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attendance.user.username} - {self.attendance.date} - {self.hours} hours"