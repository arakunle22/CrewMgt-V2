from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', user_views.landing_page, name=''),
    path('', user_views.landing_page, name='landing_page'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('crew-dashboard/', user_views.crew_dashboard, name='crew_dashboard'),
    path('manager-dashboard/', user_views.manager_dashboard, name='manager_dashboard'),
    path('admin-approval/', user_views.admin_approval, name='admin_approval'),
]




