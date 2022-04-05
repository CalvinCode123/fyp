from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django import template
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher_name = models.CharField(max_length=100)

class Classroom(models.Model):
    classroom_subject = models.CharField(max_length=100)
    classroom_code = models.CharField(max_length= 5, default = '00000')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classroom_description = models.TextField()
    def __str__(self):
        return self.classroom_subject

    def get_student(self):
        return 

    def get_classroom(self):
        workitems = WorkItem.objects.filter(classroom = self).count()
        return workitems

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classroom, blank = True)

class WorkItem(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    work_description = models.TextField()

    date_assigned = models.DateField(auto_now_add=True, blank=True)
    time_assigned = models.TimeField(auto_now_add=True, blank=True)

    @property
    def get_age(self):
        return int((timezone.now() - self.date_assigned).total_seconds()/3600)

    def get_classroom(self):
        return self.classroom.classroom_subject

    def get_date(self):
        return self.date_assigned

class UserUpload(models.Model):
    name = models.CharField(max_length= 30)
    picture = models.FileField(upload_to='media/',  validators=[FileExtensionValidator( ['pdf', 'dox', 'png', 'jpg', 'jpeg', 'docx'] ) ])
    date = models.DateField()
    time_assigned = models.TimeField(auto_now_add=True, blank=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classtrail_bool = models.BooleanField('Add to ClassTrail', default=True)
    submission = models.ForeignKey(WorkItem, null = True, on_delete=models.CASCADE)
    grade = models.IntegerField(null = True, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])

    def delete(self):
        self.picture.delete(save=False)
        super().delete()

    @property
    def is_late(self):
        if self.submission is not None:
            assigned_date = datetime.combine(self.submission.date_assigned, self.submission.time_assigned)
            submission_date = datetime.combine(self.date, self.submission.time_assigned)
            return submission_date
            


    