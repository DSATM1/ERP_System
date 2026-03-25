"""
Student views - Student management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Student
from .forms import StudentRegistrationForm, StudentUpdateForm


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    ordering = ['roll_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user', 'course', 'course__department')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(roll_number__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        # Filter by course
        course_id = self.request.GET.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Filter by semester
        semester = self.request.GET.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_course'] = self.request.GET.get('course', '')
        context['selected_semester'] = self.request.GET.get('semester', '')
        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form):
        messages.success(self.request, f'Student registered successfully!')
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form):
        messages.success(self.request, f'Student "{self.object.roll_number}" updated successfully!')
        return super().form_valid(form)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = self.object.get_current_semester_subjects()
        return context


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form):
        messages.success(self.request, f'Student "{self.object.roll_number}" deleted successfully!')
        return super().form_valid(form)