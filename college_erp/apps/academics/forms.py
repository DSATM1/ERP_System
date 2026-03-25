"""
Academic forms - Department, Course, and Subject forms.
"""
from django import forms
from .models import Department, Course, Semester, Subject


class DepartmentForm(forms.ModelForm):
    """Form for creating/editing departments."""

    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CSE, ECE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head': forms.Select(attrs={'class': 'form-select'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CourseForm(forms.ModelForm):
    """Form for creating/editing courses."""

    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'course_type', 'duration_years',
                  'total_semesters', 'description', 'eligibility', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BTECH-CSE'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'course_type': forms.Select(attrs={'class': 'form-select'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'total_semesters': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'eligibility': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SemesterForm(forms.ModelForm):
    """Form for creating/editing semesters."""

    class Meta:
        model = Semester
        fields = ['semester_number', 'course', 'start_month', 'end_month']
        widgets = {
            'semester_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'start_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'end_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
        }


class SubjectForm(forms.ModelForm):
    """Form for creating/editing subjects."""

    class Meta:
        model = Subject
        fields = ['name', 'code', 'semester', 'subject_type', 'credits',
                  'theory_hours', 'practical_hours', 'max_marks', 'passing_marks', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS101'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'subject_type': forms.Select(attrs={'class': 'form-select'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'theory_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'practical_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }