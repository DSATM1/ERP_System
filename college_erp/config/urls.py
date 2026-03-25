"""
URL configuration for College ERP project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('academics/', include('apps.academics.urls', namespace='academics')),
    path('students/', include('apps.students.urls', namespace='students')),
    path('faculty/', include('apps.faculty.urls', namespace='faculty')),
    path('attendance/', include('apps.attendance.urls', namespace='attendance')),
    path('examination/', include('apps.examination.urls', namespace='examination')),
    path('timetable/', include('apps.timetable.urls', namespace='timetable')),
    path('fees/', include('apps.fees.urls', namespace='fees')),
    path('library/', include('apps.library.urls', namespace='library')),
    path('hostel/', include('apps.hostel.urls', namespace='hostel')),
    path('transport/', include('apps.transport.urls', namespace='transport')),
    path('announcements/', include('apps.announcements.urls', namespace='announcements')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)