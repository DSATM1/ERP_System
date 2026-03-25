"""
Faculty forms - Faculty registration and profile forms.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import CustomUser
from .models import Faculty


class FacultyRegistrationForm(forms.ModelForm):
    """Form for faculty registration with user details."""

    # User fields
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False)

    class Meta:
        model = Faculty
        fields = [
            'employee_id', 'department', 'designation', 'employment_type',
            'joining_date', 'experience_years', 'qualification', 'specialization',
            'publications', 'salary', 'research_interests', 'achievements'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'publications': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'research_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def save(self, commit=True):
        faculty = super().save(commit=False)
        # Create user first
        user = CustomUser.objects.create_user(
            username=self.cleaned_data.get('employee_id', faculty.employee_id),
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data.get('phone_number'),
            date_of_birth=self.cleaned_data.get('date_of_birth'),
            gender=self.cleaned_data.get('gender'),
            address=self.cleaned_data.get('address'),
            role='faculty'
        )
        faculty.user = user
        if commit:
            user.save()
            faculty.save()
        return faculty


class FacultyUpdateForm(forms.ModelForm):
    """Form for updating faculty details."""

    class Meta:
        model = Faculty
        fields = [
            'employee_id', 'department', 'designation', 'employment_type',
            'joining_date', 'experience_years', 'qualification', 'specialization',
            'publications', 'salary', 'research_interests', 'achievements', 'is_active'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'publications': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'research_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }