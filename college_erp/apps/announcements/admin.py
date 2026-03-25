from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'publish_date', 'is_pinned', 'is_active']
    list_filter = ['category', 'priority', 'is_pinned', 'is_active', 'publish_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'publish_date'