"""
Examination URLs - URL patterns for exam management.
"""
from django.urls import path
from .views import ExamListView, ExamCreateView, ExamDetailView, ResultListView, student_results

app_name = 'examination'

urlpatterns = [
    path('exams/', ExamListView.as_view(), name='exam_list'),
    path('exams/create/', ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam_detail'),
    path('results/', ResultListView.as_view(), name='result_list'),
    path('results/student/<int:student_id>/', student_results, name='student_results'),
]