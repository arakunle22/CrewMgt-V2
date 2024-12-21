# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('leave/', views.leave_management, name='leave_management'),
]