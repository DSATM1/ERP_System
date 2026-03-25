from django.contrib import admin
from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'designation', 'joining_date', 'is_active']
    list_filter = ['department', 'designation', 'employment_type', 'is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['employee_id']
    raw_id_fields = ['user', 'department']