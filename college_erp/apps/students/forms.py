"""
Student forms - Student registration and profile forms.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import CustomUser
from .models import Student


class StudentRegistrationForm(forms.ModelForm):
    """Form for student registration with user details."""

    # User fields
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Student
        fields = [
            'roll_number', 'course', 'semester', 'batch',
            'father_name', 'father_occupation', 'father_phone',
            'mother_name', 'mother_occupation', 'mother_phone',
            'blood_group', 'category', 'nationality', 'religion', 'aadhaar_number',
            'permanent_address', 'current_address',
            'emergency_contact_name', 'emergency_contact_relation', 'emergency_contact_phone'
        ]
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2023-2027'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        student = super().save(commit=False)
        # Create user first
        user = CustomUser.objects.create_user(
            username=self.cleaned_data.get('roll_number', student.roll_number),
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data.get('phone_number'),
            date_of_birth=self.cleaned_data.get('date_of_birth'),
            gender=self.cleaned_data.get('gender'),
            role='student'
        )
        student.user = user
        if commit:
            user.save()
            student.save()
        return student


class StudentUpdateForm(forms.ModelForm):
    """Form for updating student details."""

    class Meta:
        model = Student
        fields = [
            'roll_number', 'course', 'semester', 'batch',
            'father_name', 'father_occupation', 'father_phone',
            'mother_name', 'mother_occupation', 'mother_phone',
            'blood_group', 'category', 'nationality', 'religion', 'aadhaar_number',
            'permanent_address', 'current_address',
            'emergency_contact_name', 'emergency_contact_relation', 'emergency_contact_phone',
            'is_active'
        ]
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }