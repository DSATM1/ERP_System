"""
Account URLs - URL patterns for user authentication and profile management.
"""
from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    dashboard,
    UserCreateView,
    UserUpdateView,
    profile,
    user_list
)

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # User Management
    path('users/', user_list, name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('profile/<int:pk>/', profile, name='profile'),
]