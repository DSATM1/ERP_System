"""
Student models - Student profile and academic information.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, ActiveModel
from apps.core.utils import generate_unique_id


class Student(TimeStampedModel, ActiveModel):
    """
    Student model - Extended profile for students.
    """

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('ews', 'EWS'),
    ]

    # Link to CustomUser
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    # Academic Information
    roll_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=50, unique=True, blank=True)
    admission_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(
        'academics.Course',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    semester = models.PositiveIntegerField(default=1)
    batch = models.CharField(max_length=20, help_text='e.g., 2023-2027')

    # Personal Information
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    # Additional Details
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    nationality = models.CharField(max_length=50, default='Indian')
    religion = models.CharField(max_length=50, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)

    # Contact Information
    permanent_address = models.TextField()
    current_address = models.TextField(blank=True, null=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['roll_number']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.roll_number:
            # Generate unique roll number
            prefix = self.course.code if self.course else 'STU'
            self.roll_number = generate_unique_id(prefix, 6)
        if not self.registration_number:
            self.registration_number = f"REG{self.roll_number}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def phone(self):
        return self.user.phone_number

    def get_current_semester_subjects(self):
        """Get all subjects for current semester."""
        if self.course:
            from apps.academics.models import Subject, Semester
            try:
                semester = Semester.objects.get(course=self.course, semester_number=self.semester)
                return Subject.objects.filter(semester=semester, is_active=True)
            except Semester.DoesNotExist:
                return []
        return []