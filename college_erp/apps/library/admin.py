from django.contrib import admin
from .models import BookCategory, Book, BookIssue


admin.site.register(BookCategory)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'total_copies', 'available_copies', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'author', 'isbn']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'issue_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status', 'issue_date']
    search_fields = ['book__title', 'student__roll_number']
    date_hierarchy = 'issue_date'