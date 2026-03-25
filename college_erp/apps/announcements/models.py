"""
Announcements models - Notices and announcements.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Announcement(TimeStampedModel):
    """College announcements and notices."""

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('exam', 'Examination'),
        ('event', 'Event'),
        ('holiday', 'Holiday'),
        ('sports', 'Sports'),
        ('placement', 'Placement'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_pinned = models.BooleanField(default=False)
    publish_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    target_audience = models.CharField(max_length=20, blank=True, null=True,
                                       help_text='all, students, faculty, staff')
    attachment = models.FileField(upload_to='announcements/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_pinned', '-publish_date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title

    @property
    def priority_color(self):
        colors = {
            'low': 'info',
            'medium': 'primary',
            'high': 'warning',
            'urgent': 'danger'
        }
        return colors.get(self.priority, 'secondary')