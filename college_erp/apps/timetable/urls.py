from django.urls import path
from django.views.generic import ListView
from .models import Timetable

app_name = 'timetable'

urlpatterns = [
    path('', ListView.as_view(model=Timetable, template_name='timetable/timetable_list.html', context_object_name='timetables'), name='timetable_list'),
]