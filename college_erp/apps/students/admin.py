from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'user', 'course', 'semester', 'batch', 'is_active']
    list_filter = ['course', 'semester', 'batch', 'is_active', 'category']
    search_fields = ['roll_number', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['roll_number']
    raw_id_fields = ['user', 'course']