from django.contrib import admin
from .models import TimeSlot, Room, Timetable


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['slot_number', 'start_time', 'end_time']
    ordering = ['slot_number']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'capacity', 'building', 'is_available']
    list_filter = ['room_type', 'is_available']
    search_fields = ['room_number', 'building']


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course', 'semester', 'day', 'time_slot', 'subject', 'faculty', 'room']
    list_filter = ['course', 'semester', 'day']
    search_fields = ['subject__code', 'faculty__employee_id']