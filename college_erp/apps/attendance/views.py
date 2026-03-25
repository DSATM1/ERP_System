"""
Attendance views - Attendance management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from datetime import date, timedelta

from .models import Attendance, AttendanceReport


class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('student__user', 'subject')
        return queryset


class MarkAttendanceView(TemplateView):
    template_name = 'attendance/mark_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


@login_required
def student_attendance_report(request, student_id):
    """View attendance report for a specific student."""
    from apps.students.models import Student
    student = get_object_or_404(Student, pk=student_id)
    reports = AttendanceReport.objects.filter(student=student).select_related('subject')

    return render(request, 'attendance/attendance_report.html', {
        'student': student,
        'reports': reports
    })