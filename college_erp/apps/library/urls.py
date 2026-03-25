from django.urls import path
from django.views.generic import ListView
from .models import Book, BookIssue

app_name = 'library'

urlpatterns = [
    path('books/', ListView.as_view(model=Book, template_name='library/book_list.html', context_object_name='books'), name='book_list'),
    path('issues/', ListView.as_view(model=BookIssue, template_name='library/issue_list.html', context_object_name='issues'), name='issue_list'),
]