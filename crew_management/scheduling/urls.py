from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shift-schedule/', views.shift_schedule, name='shift_schedule'),
    path('availability/', views.availability, name='availability'),
]