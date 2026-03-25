from django.urls import path
from django.views.generic import ListView
from .models import Route, Vehicle

app_name = 'transport'

urlpatterns = [
    path('routes/', ListView.as_view(model=Route, template_name='transport/route_list.html', context_object_name='routes'), name='route_list'),
    path('vehicles/', ListView.as_view(model=Vehicle, template_name='transport/vehicle_list.html', context_object_name='vehicles'), name='vehicle_list'),
]