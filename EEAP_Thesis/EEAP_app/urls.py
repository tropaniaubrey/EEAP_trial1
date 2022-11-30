from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('student_registration', views.student_registration, name='student_registration'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('vehicle_registration', views.vehicle_registration, name='vehicle_registration'),
    path('registered_vehicle', views.registered_vehicle, name='registered_vehicle'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('pending_vehicle', views.pending_vehicle, name='pending_vehicle'),
    path('logout', views.logoutuser, name='logout'),

]