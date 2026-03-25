"""
Examination views - Exam and result management.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Exam, ExamSchedule, Result


class ExamListView(ListView):
    model = Exam
    template_name = 'examination/exam_list.html'
    context_object_name = 'exams'
    ordering = ['-start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('course', 'semester')
        return queryset


class ExamCreateView(CreateView):
    model = Exam
    fields = ['name', 'exam_type', 'course', 'semester', 'start_date', 'end_date',
              'total_marks', 'passing_marks', 'description']
    template_name = 'examination/exam_form.html'
    success_url = reverse_lazy('examination:exam_list')

    def form_valid(self, form):
        messages.success(self.request, f'Exam "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'examination/exam_detail.html'
    context_object_name = 'exam'


class ResultListView(ListView):
    model = Result
    template_name = 'examination/result_list.html'
    context_object_name = 'results'
    ordering = ['-exam', 'student']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('student__user', 'exam', 'subject')
        return queryset


@login_required
def student_results(request, student_id):
    """View results for a specific student."""
    from apps.students.models import Student
    student = get_object_or_404(Student, pk=student_id)
    results = Result.objects.filter(student=student).select_related('exam', 'subject')

    return render(request, 'examination/student_results.html', {
        'student': student,
        'results': results
    })