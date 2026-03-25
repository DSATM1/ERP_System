"""
Core models - Base models used across all apps.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at fields.
    All models should inherit from this to track when records were created/modified.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """
    Abstract base model that provides is_active field for soft delete functionality.
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the record by setting is_active to False."""
        self.is_active = False
        self.save(update_fields=['is_active'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_active = True
        self.save(update_fields=['is_active'])