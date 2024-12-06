from django.contrib import admin
from .models import Shift, Schedule, Availability

admin.site.register(Shift)
admin.site.register(Schedule)
admin.site.register(Availability)
