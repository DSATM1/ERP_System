from django.urls import path
from django.views.generic import ListView
from .models import FeePayment

app_name = 'fees'

urlpatterns = [
    path('', ListView.as_view(model=FeePayment, template_name='fees/fee_list.html', context_object_name='payments'), name='fee_list'),
]