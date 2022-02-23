from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Teacher, Student, User

class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    #teacher_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ['first_name', 'last_name', 'teacher_name']

    field_order = ['username','first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic #if block of code succesfully run, changes are saved. Changes rolled back if there is an exception
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()#saving in user table
        teacher = Teacher.objects.create(user=user)
        teacher.teacher_name = self.cleaned_data.get('teacher_name')
        teacher.save()
        return user

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    #student_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ['first_name', 'last_name', 'student_name']
    field_order = ['username','first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic #if block of code succesfully run, changes are saved. Changes rolled back if there is an exception
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()#saving in user table
        student = Student.objects.create(user=user)
        student.student_name = self.cleaned_data.get('student_name')# data passed to server as string. clean data converts to appropriate type
        student.save()
        return user