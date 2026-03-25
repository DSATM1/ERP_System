from django.urls import path
from django.views.generic import ListView
from .models import HostelBlock, Room

app_name = 'hostel'

urlpatterns = [
    path('', ListView.as_view(model=HostelBlock, template_name='hostel/hostel_list.html', context_object_name='hostels'), name='hostel_list'),
    path('rooms/', ListView.as_view(model=Room, template_name='hostel/room_list.html', context_object_name='rooms'), name='room_list'),
]