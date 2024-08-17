

from django.urls import path
from . import views


from django.urls import path, include


# monitoring/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.Sample, name='dashboard'),
    path('Sample/', views.Sample, name='Sample'),
    path('api/receive/', views.receive_data, name='receive_data'),
    path('toggle_aerator/', views.toggle_aerator, name='toggle_aerator'),
    
]
