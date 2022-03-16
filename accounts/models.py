from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classroom, blank = True)

class WorkItem(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    work_description = models.CharField(max_length=500)

