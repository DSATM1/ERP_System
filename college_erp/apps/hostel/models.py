"""
Hostel models - Room management and allotments.
"""
from django.db import models
from apps.core.models import TimeStampedModel, ActiveModel


class HostelBlock(TimeStampedModel, ActiveModel):
    """Hostel block/building."""
    BLOCK_TYPES = [
        ('boys', 'Boys Hostel'),
        ('girls', 'Girls Hostel'),
    ]

    name = models.CharField(max_length=100)
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES)
    warden = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='hostel_blocks')
    total_rooms = models.PositiveIntegerField(default=0)
    total_capacity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Hostel Block'
        verbose_name_plural = 'Hostel Blocks'

    def __str__(self):
        return f"{self.name} ({self.get_block_type_display()})"


class Room(TimeStampedModel, ActiveModel):
    """Hostel room details."""
    ROOM_TYPES = [
        ('single', 'Single Occupancy'),
        ('double', 'Double Occupancy'),
        ('triple', 'Triple Occupancy'),
        ('dormitory', 'Dormitory'),
    ]

    hostel_block = models.ForeignKey(HostelBlock, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.PositiveIntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='double')
    capacity = models.PositiveIntegerField(default=2)
    current_occupancy = models.PositiveIntegerField(default=0)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['hostel_block', 'room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        unique_together = ['hostel_block', 'room_number']

    def __str__(self):
        return f"{self.hostel_block.name} - Room {self.room_number}"

    @property
    def is_full(self):
        return self.current_occupancy >= self.capacity


class RoomAllotment(TimeStampedModel):
    """Room allotment to students."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('vacated', 'Vacated'),
        ('transferred', 'Transferred'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='room_allotments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allotments')
    allotment_date = models.DateField()
    vacated_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-allotment_date']
        verbose_name = 'Room Allotment'
        verbose_name_plural = 'Room Allotments'

    def __str__(self):
        return f"{self.student.roll_number} - {self.room}"