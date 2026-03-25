"""
Fee models - Fee structure, payments, and receipts.
"""
from django.db import models
from apps.core.models import TimeStampedModel, ActiveModel
from apps.core.utils import generate_unique_id


class FeeCategory(TimeStampedModel):
    """Categories of fees (Tuition, Library, Lab, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Fee Category'
        verbose_name_plural = 'Fee Categories'

    def __str__(self):
        return self.name


class FeeStructure(TimeStampedModel, ActiveModel):
    """Fee structure for courses."""
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.CharField(max_length=20, help_text='e.g., 2023-2024')
    semester = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()

    class Meta:
        ordering = ['-academic_year', 'course', 'semester']
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'

    def __str__(self):
        return f"{self.course.code} - Sem {self.semester} - {self.academic_year}"


class FeeComponent(TimeStampedModel):
    """Individual fee components within a structure."""
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='components')
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Fee Component'
        verbose_name_plural = 'Fee Components'

    def __str__(self):
        return f"{self.category.name} - ₹{self.amount}"


class FeePayment(TimeStampedModel):
    """Student fee payment records."""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    receipt_number = models.CharField(max_length=20, unique=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-payment_date', 'student']
        verbose_name = 'Fee Payment'
        verbose_name_plural = 'Fee Payments'

    def __str__(self):
        return f"{self.student.roll_number} - {self.receipt_number} - ₹{self.amount_paid}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = generate_unique_id('RCP', 8)
        super().save(*args, **kwargs)