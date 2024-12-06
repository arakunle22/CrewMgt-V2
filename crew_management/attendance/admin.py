
# Register your models here.

from django.contrib import admin
from .models import Attendance, Overtime

admin.site.register(Attendance)
admin.site.register(Overtime)


