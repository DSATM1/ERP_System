"""
Examination models - Exam schedules, results, and grades.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject, Semester


class Exam(TimeStampedModel):
    """
    Exam model - Examination schedule and details.
    """

    EXAM_TYPE_CHOICES = [
        ('internal', 'Internal Assessment'),
        ('midterm', 'Mid-Term Exam'),
        ('endterm', 'End-Term Exam'),
        ('practical', 'Practical Exam'),
        ('assignment', 'Assignment'),
    ]

    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    course = models.ForeignKey(
        'academics.Course',
        on_delete=models.CASCADE,
        related_name='exams'
    )
    semester = models.ForeignKey(
        'academics.Semester',
        on_delete=models.CASCADE,
        related_name='exams'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date', 'name']
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return f"{self.name} - {self.course.code} Sem {self.semester.semester_number}"


class ExamSchedule(TimeStampedModel):
    """
    Exam Schedule - Subject-wise exam timing.
    """

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='exam_schedules'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True, null=True)
    max_marks = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Exam Schedule'
        verbose_name_plural = 'Exam Schedules'

    def __str__(self):
        return f"{self.exam.name} - {self.subject.code} - {self.date}"


class Result(TimeStampedModel):
    """
    Result model - Student exam results and grades.
    """

    GRADE_CHOICES = [
        ('O', 'O Grade (90-100%)'),
        ('A+', 'A+ Grade (80-89%)'),
        ('A', 'A Grade (70-79%)'),
        ('B+', 'B+ Grade (60-69%)'),
        ('B', 'B Grade (50-59%)'),
        ('C', 'C Grade (40-49%)'),
        ('F', 'F Grade (Below 40%)'),
    ]

    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='results'
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='results'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='results'
    )
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.PositiveIntegerField(default=100)
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True)
    is_pass = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entered_results'
    )

    class Meta:
        ordering = ['-exam', 'student', 'subject']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        unique_together = ['student', 'exam', 'subject']

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.marks_obtained}"

    def calculate_grade(self):
        """Calculate grade based on percentage."""
        percentage = (self.marks_obtained / self.max_marks) * 100
        if percentage >= 90:
            self.grade = 'O'
        elif percentage >= 80:
            self.grade = 'A+'
        elif percentage >= 70:
            self.grade = 'A'
        elif percentage >= 60:
            self.grade = 'B+'
        elif percentage >= 50:
            self.grade = 'B'
        elif percentage >= 40:
            self.grade = 'C'
        else:
            self.grade = 'F'

        self.is_pass = percentage >= 40
        return self.grade

    def save(self, *args, **kwargs):
        self.calculate_grade()
        super().save(*args, **kwargs)