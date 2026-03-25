from django.contrib import admin
from .models import Exam, ExamSchedule, Result


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'course', 'semester', 'start_date', 'end_date', 'is_active']
    list_filter = ['exam_type', 'is_active', 'course', 'semester']
    search_fields = ['name', 'course__code']
    date_hierarchy = 'start_date'


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam', 'subject', 'date', 'start_time', 'end_time', 'room']
    list_filter = ['exam', 'date']
    search_fields = ['exam__name', 'subject__code']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks_obtained', 'max_marks', 'grade', 'is_pass']
    list_filter = ['exam', 'grade', 'is_pass']
    search_fields = ['student__roll_number', 'subject__code']