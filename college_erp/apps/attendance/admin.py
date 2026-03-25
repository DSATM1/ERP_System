from django.contrib import admin
from .models import Attendance, AttendanceReport


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date', 'subject']
    search_fields = ['student__roll_number', 'student__user__first_name']
    date_hierarchy = 'date'


class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'month', 'year', 'total_classes', 'attendance_percentage']
    list_filter = ['month', 'year', 'subject']
    search_fields = ['student__roll_number']


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(AttendanceReport, AttendanceReportAdmin)