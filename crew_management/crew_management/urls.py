from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
    path('', include('attendance.urls')),
    path('', include('task_management.urls')),
    path('', include('scheduling.urls')),
    path('', include('leave_management.urls')),
]
