"""
Attendance URLs - URL patterns for attendance management.
"""
from django.urls import path
from .views import AttendanceListView, MarkAttendanceView, student_attendance_report

app_name = 'attendance'

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance_list'),
    path('mark/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('report/<int:student_id>/', student_attendance_report, name='attendance_report'),
]