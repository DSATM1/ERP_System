"""
Faculty views - Faculty management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Faculty
from .forms import FacultyRegistrationForm, FacultyUpdateForm


class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculty/faculty_list.html'
    context_object_name = 'faculty_members'
    ordering = ['employee_id']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user', 'department')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(employee_id__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        # Filter by department
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # Filter by designation
        designation = self.request.GET.get('designation')
        if designation:
            queryset = queryset.filter(designation=designation)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_designation'] = self.request.GET.get('designation', '')
        return context


class FacultyCreateView(CreateView):
    model = Faculty
    form_class = FacultyRegistrationForm
    template_name = 'faculty/faculty_form.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, f'Faculty member registered successfully!')
        return super().form_valid(form)


class FacultyUpdateView(UpdateView):
    model = Faculty
    form_class = FacultyUpdateForm
    template_name = 'faculty/faculty_form.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, f'Faculty member "{self.object.employee_id}" updated successfully!')
        return super().form_valid(form)


class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'faculty/faculty_detail.html'
    context_object_name = 'faculty_member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assigned_subjects'] = self.object.get_assigned_subjects()
        return context


class FacultyDeleteView(DeleteView):
    model = Faculty
    template_name = 'faculty/faculty_confirm_delete.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, f'Faculty member "{self.object.employee_id}" deleted successfully!')
        return super().form_valid(form)