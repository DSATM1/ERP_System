"""
Academic models - Department, Course, Semester, Subject.
"""
from django.db import models
from apps.core.models import TimeStampedModel, ActiveModel


class Department(TimeStampedModel, ActiveModel):
    """
    Academic Department model.
    Represents various departments in the college (e.g., Computer Science, Electronics).
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_department',
        verbose_name='Department Head'
    )
    established_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_course_count(self):
        """Return the number of courses in this department."""
        return self.courses.count()

    def get_faculty_count(self):
        """Return the number of faculty in this department."""
        return self.faculty_members.count()


class Course(TimeStampedModel, ActiveModel):
    """
    Course/Program model.
    Represents degree programs like B.Tech, B.Sc, M.Tech, etc.
    """

    COURSE_TYPES = [
        ('ug', 'Undergraduate'),
        ('pg', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='ug')
    duration_years = models.PositiveIntegerField(default=4, verbose_name='Duration (Years)')
    total_semesters = models.PositiveIntegerField(default=8)
    description = models.TextField(blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True, help_text='Eligibility criteria')

    class Meta:
        ordering = ['department__name', 'name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_student_count(self):
        """Return the number of students enrolled in this course."""
        return self.students.count()


class Semester(TimeStampedModel):
    """
    Semester model.
    Represents academic semesters (1st, 2nd, 3rd, etc.).
    """

    semester_number = models.PositiveIntegerField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='semesters'
    )
    start_month = models.PositiveIntegerField(default=1, help_text='Month when semester starts (1-12)')
    end_month = models.PositiveIntegerField(default=6, help_text='Month when semester ends (1-12)')

    class Meta:
        ordering = ['course', 'semester_number']
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        unique_together = ['course', 'semester_number']

    def __str__(self):
        return f"Semester {self.semester_number} - {self.course.name}"

    def get_name(self):
        """Return human-readable semester name."""
        ordinal = ['', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        if 1 <= self.semester_number <= 10:
            return f"{ordinal[self.semester_number]} Semester"
        return f"Semester {self.semester_number}"


class Subject(TimeStampedModel, ActiveModel):
    """
    Subject model.
    Represents individual subjects/courses taught in a semester.
    """

    SUBJECT_TYPES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('lab', 'Laboratory'),
        ('project', 'Project'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES, default='theory')
    credits = models.PositiveIntegerField(default=3, help_text='Credit hours for this subject')
    theory_hours = models.PositiveIntegerField(default=3, help_text='Theory hours per week')
    practical_hours = models.PositiveIntegerField(default=0, help_text='Practical hours per week')
    max_marks = models.PositiveIntegerField(default=100, verbose_name='Maximum Marks')
    passing_marks = models.PositiveIntegerField(default=40, verbose_name='Passing Marks')

    class Meta:
        ordering = ['semester', 'code']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def total_hours(self):
        """Return total hours per week."""
        return self.theory_hours + self.practical_hours