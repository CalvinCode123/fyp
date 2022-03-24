from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone

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
    
    def __str__(self):
        return self.classroom_subject

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classroom, blank = True)



class UserUpload(models.Model):
    name = models.CharField(max_length= 30)
    picture = models.FileField(upload_to='media/')
    date = models.DateTimeField()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def delete(self):
        self.picture.delete(save=False)
        super().delete()

class WorkItem(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    work_description = models.CharField(max_length=500)
    date_assigned = models.DateField(auto_now_add=True, blank=True)
    time_assigned = models.TimeField(auto_now_add=True, blank=True)
    submission = models.ForeignKey(UserUpload, null = True, on_delete=models.CASCADE)

    @property
    def get_age(self):
        return int((timezone.now() - self.date_assigned).total_seconds()/3600)

    def get_classroom(self):
        return self.classroom.classroom_subject