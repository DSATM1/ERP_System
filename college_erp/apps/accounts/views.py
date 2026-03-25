"""
Account views - Login, logout, profile management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from .forms import CustomUserCreationForm, UserProfileForm, CustomLoginForm
from .models import CustomUser


class CustomLoginView(LoginView):
    """Custom login view."""
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name()}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('accounts:login')


@login_required
def dashboard(request):
    """
    Main dashboard view - redirects to role-specific dashboard.
    """
    user = request.user

    context = {
        'user': user,
    }

    # Add role-specific context
    if user.is_admin:
        context['total_students'] = CustomUser.objects.filter(role='student', is_active=True).count()
        context['total_faculty'] = CustomUser.objects.filter(role='faculty', is_active=True).count()
        context['total_staff'] = CustomUser.objects.filter(role='staff', is_active=True).count()
        return render(request, 'accounts/admin_dashboard.html', context)

    elif user.is_faculty:
        return render(request, 'accounts/faculty_dashboard.html', context)

    elif user.is_student:
        return render(request, 'accounts/student_dashboard.html', context)

    else:
        return render(request, 'accounts/staff_dashboard.html', context)


class UserCreateView(CreateView):
    """View for creating new users (admin only)."""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.username} created successfully!')
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """View for updating user profile."""
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/user_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


@login_required
def profile(request, pk):
    """View user profile."""
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/profile.html', {'profile_user': user})


@login_required
def user_list(request):
    """List all users (admin only)."""
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')

    users = CustomUser.objects.all().select_related()
    return render(request, 'accounts/user_list.html', {'users': users})