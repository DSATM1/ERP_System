"""
Faculty URLs - URL patterns for faculty management.
"""
from django.urls import path
from .views import (
    FacultyListView, FacultyCreateView, FacultyUpdateView,
    FacultyDetailView, FacultyDeleteView
)

app_name = 'faculty'

urlpatterns = [
    path('', FacultyListView.as_view(), name='faculty_list'),
    path('create/', FacultyCreateView.as_view(), name='faculty_create'),
    path('<int:pk>/', FacultyDetailView.as_view(), name='faculty_detail'),
    path('<int:pk>/edit/', FacultyUpdateView.as_view(), name='faculty_edit'),
    path('<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty_delete'),
]