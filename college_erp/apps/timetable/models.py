"""
Timetable models - Class schedules and room allocation.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class TimeSlot(TimeStampedModel):
    """Time slots for classes."""
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['slot_number']
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        return f"Slot {self.slot_number}: {self.start_time} - {self.end_time}"


class Room(TimeStampedModel):
    """Classroom/Lab information."""
    ROOM_TYPES = [
        ('classroom', 'Classroom'),
        ('lab', 'Laboratory'),
        ('seminar', 'Seminar Hall'),
        ('auditorium', 'Auditorium'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='classroom')
    capacity = models.PositiveIntegerField(default=60)
    building = models.CharField(max_length=100, blank=True, null=True)
    floor = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"{self.room_number} ({self.get_room_type_display()})"


class Timetable(TimeStampedModel):
    """Class schedule/timetable."""
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
    ]

    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='timetables')
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE, related_name='timetables')
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='timetables')
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, related_name='timetables')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='timetables')

    class Meta:
        ordering = ['day', 'time_slot__slot_number']
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable'
        unique_together = ['course', 'semester', 'day', 'time_slot']

    def __str__(self):
        return f"{self.course.code} Sem {self.semester.semester_number} - {self.get_day_display()} Slot {self.time_slot.slot_number}"

    def get_day_display(self):
        return dict(self.DAYS_OF_WEEK).get(self.day, '')