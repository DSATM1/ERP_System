"""
Library models - Books, issues, and returns.
"""
from django.db import models
from apps.core.models import TimeStampedModel, ActiveModel
from apps.core.utils import generate_unique_id
from datetime import date, timedelta


class BookCategory(TimeStampedModel):
    """Book categories/genres."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Book Category'
        verbose_name_plural = 'Book Categories'

    def __str__(self):
        return self.name


class Book(TimeStampedModel, ActiveModel):
    """Book details."""
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, related_name='books')
    publication_year = models.PositiveIntegerField(blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    shelf_location = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.available_copies > 0


class BookIssue(TimeStampedModel):
    """Book issue records."""
    ISSUE_STATUS = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField(default=date.today)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ISSUE_STATUS, default='issued')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Book Issue'
        verbose_name_plural = 'Book Issues'

    def __str__(self):
        return f"{self.book.title} - {self.student.roll_number}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            # Default issue period: 14 days
            self.due_date = date.today() + timedelta(days=14)
        super().save(*args, **kwargs)

    def calculate_fine(self):
        """Calculate fine for overdue books."""
        if self.status == 'overdue' and self.return_date:
            days_overdue = (self.return_date - self.due_date).days
            # Fine: ₹5 per day
            self.fine_amount = max(0, days_overdue * 5)
        return self.fine_amount