from django.contrib import admin
from .models import FeeCategory, FeeStructure, FeeComponent, FeePayment


admin.site.register(FeeCategory)
admin.site.register(FeeStructure)
admin.site.register(FeeComponent)


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'receipt_number', 'amount_paid', 'payment_date', 'payment_method', 'status']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['student__roll_number', 'receipt_number', 'transaction_id']
    date_hierarchy = 'payment_date'