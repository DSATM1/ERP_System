"""
Academic views - Department, Course, and Subject management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count

from .models import Department, Course, Semester, Subject
from .forms import DepartmentForm, CourseForm, SemesterForm, SubjectForm


# Department Views
class DepartmentListView(ListView):
    model = Department
    template_name = 'academics/department_list.html'
    context_object_name = 'departments'
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            course_count=Count('courses'),
            faculty_count=Count('faculty_members')
        )
        if not self.request.user.is_admin:
            queryset = queryset.filter(is_active=True)
        return queryset


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/department_form.html'
    success_url = reverse_lazy('academics:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'Department "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/department_form.html'
    success_url = reverse_lazy('academics:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'Department "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'academics/department_confirm_delete.html'
    success_url = reverse_lazy('academics:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'Department "{self.object.name}" deleted successfully!')
        return super().form_valid(form)


# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'
    ordering = ['department__name', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('department')
        if not self.request.user.is_admin:
            queryset = queryset.filter(is_active=True)
        return queryset


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/course_form.html'
    success_url = reverse_lazy('academics:course_list')

    def form_valid(self, form):
        messages.success(self.request, f'Course "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/course_form.html'
    success_url = reverse_lazy('academics:course_list')

    def form_valid(self, form):
        messages.success(self.request, f'Course "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'academics/course_confirm_delete.html'
    success_url = reverse_lazy('academics:course_list')

    def form_valid(self, form):
        messages.success(self.request, f'Course "{self.object.name}" deleted successfully!')
        return super().form_valid(form)


# Subject Views
class SubjectListView(ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'
    ordering = ['semester__course', 'semester__semester_number', 'code']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('semester__course')
        if not self.request.user.is_admin:
            queryset = queryset.filter(is_active=True)
        return queryset


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')

    def form_valid(self, form):
        messages.success(self.request, f'Subject "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')

    def form_valid(self, form):
        messages.success(self.request, f'Subject "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'academics/subject_confirm_delete.html'
    success_url = reverse_lazy('academics:subject_list')

    def form_valid(self, form):
        messages.success(self.request, f'Subject "{self.object.name}" deleted successfully!')
        return super().form_valid(form)