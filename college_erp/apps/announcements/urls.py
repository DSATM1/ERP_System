from django.urls import path
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Announcement

app_name = 'announcements'


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'
    ordering = ['-is_pinned', '-publish_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            queryset = queryset.filter(is_active=True)
        return queryset


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'content', 'category', 'priority', 'is_pinned', 'publish_date', 'expiry_date', 'attachment']
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcements:announcement_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Announcement created successfully!')
        return super().form_valid(form)


urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path('create/', AnnouncementCreateView.as_view(), name='announcement_create'),
]