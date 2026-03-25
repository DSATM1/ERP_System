"""
Attendance models - Student attendance tracking.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject


class Attendance(TimeStampedModel):
    """
    Attendance model - Daily attendance records for students.
    """

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendances'
    )

    class Meta:
        ordering = ['-date', 'student', 'subject']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student.roll_number} - {self.date} - {self.get_status_display()}"


class AttendanceReport(models.Model):
    """
    Attendance Report - Monthly/semester-wise attendance summary.
    """
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_reports'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='attendance_reports'
    )
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    total_classes = models.PositiveIntegerField(default=0)
    present_count = models.PositiveIntegerField(default=0)
    absent_count = models.PositiveIntegerField(default=0)
    late_count = models.PositiveIntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['-year', '-month', 'student']
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'
        unique_together = ['student', 'subject', 'month', 'year']

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.month}/{self.year}"

    def calculate_percentage(self):
        """Calculate attendance percentage."""
        if self.total_classes > 0:
            self.attendance_percentage = (self.present_count / self.total_classes) * 100
        else:
            self.attendance_percentage = 0
        return self.attendance_percentage