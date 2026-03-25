from django.contrib import admin
from .models import Department, Course, Semester, Subject


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'head', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'course_type', 'duration_years', 'total_semesters', 'is_active']
    list_filter = ['department', 'course_type', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['department__name', 'name']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester_number', 'course', 'get_name']
    list_filter = ['course']
    ordering = ['course', 'semester_number']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'semester', 'subject_type', 'credits', 'max_marks', 'is_active']
    list_filter = ['semester__course', 'subject_type', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['semester__course', 'semester__semester_number', 'code']