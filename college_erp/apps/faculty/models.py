"""
Faculty models - Faculty profile and academic information.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, ActiveModel
from apps.core.utils import generate_unique_id


class Faculty(TimeStampedModel, ActiveModel):
    """
    Faculty model - Extended profile for faculty members.
    """

    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'Head of Department'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('visiting', 'Visiting'),
        ('contract', 'Contract'),
    ]

    # Link to CustomUser
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='faculty_profile'
    )

    # Employment Information
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        related_name='faculty_members'
    )
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES, default='lecturer')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    joining_date = models.DateField()
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Experience (Years)')

    # Qualification
    qualification = models.CharField(max_length=200, help_text='e.g., Ph.D, M.Tech, M.Sc')
    specialization = models.CharField(max_length=200, blank=True, null=True)
    publications = models.PositiveIntegerField(default=0, verbose_name='Research Publications')

    # Salary Information
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Additional Information
    research_interests = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty Members'

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            prefix = 'FAC'
            self.employee_id = generate_unique_id(prefix, 6)
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

    def get_assigned_subjects(self):
        """Get subjects assigned to this faculty."""
        return self.assigned_subjects.filter(is_active=True)

    def get_designation_display(self):
        return dict(self.DESIGNATION_CHOICES).get(self.designation, self.designation)