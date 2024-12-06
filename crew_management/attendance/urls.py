from django.urls import path
from .views import attendance_list, attendance_detail, clock_in, clock_out, time_tracking, clock_action, clock_in_out

urlpatterns = [
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/<int:pk>/', attendance_detail, name='attendance_detail'),
    path('clock-in/', clock_in, name='clock_in'),
    path('clock-out/', clock_out, name='clock_out'),
    path('time-tracking/', time_tracking, name='time_tracking'),
    path('clock-action/', clock_action, name='clock_action'),
    path('clock-in-out/', clock_in_out, name='clock_in_out'),
]
