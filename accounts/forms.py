from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Teacher, Student, User, Classroom, WorkItem, UserUpload
from django.core.exceptions import ValidationError
import pathlib
import os.path

class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

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
        #teacher.teacher_name = self.cleaned_data.get('teacher_name')
        teacher.save()
        return user

class JoinClassroomForm(forms.Form):
    classroom_id = forms.CharField(label = "classroom ID", max_length = "10")
    classroom_code = forms.CharField(label = "classroom Code", max_length = "5")

    def clean(self):
        data = self.cleaned_data
        id = data['classroom_id']
        code = data['classroom_code']
        if not Classroom.objects.filter(id = id).exists():
            raise ValidationError({'classroom_id':["Classroom does not exist"]})
        else:
            room = Classroom.objects.get(id = id)
            if code == room.classroom_code:
                print("correct code")
            else:
                raise ValidationError({'classroom_code':["Incorrect code"]})

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

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
        #student.student_name = self.cleaned_data.get('student_name')# data passed to server as string. clean data converts to appropriate type
        student.save()
        return user

class CreateClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields= ['classroom_subject','classroom_code', 'classroom_description']
    
    def clean(self):
        data = self.cleaned_data
        code = data['classroom_code']
        if code.isdigit()==False:
            raise ValidationError({'classroom_code':["Classroom code must only contain numbers and can only be 5 digits long"]})


class CreateWorkItemForm(forms.ModelForm):
    class Meta:
        model = WorkItem
        fields= ['classroom','work_description']

    def __init__(self, user=None, **kwargs):
        super(CreateWorkItemForm, self).__init__(**kwargs)
        if user:
            self.fields['classroom'].queryset = Classroom.objects.filter(teacher_id=user)

class UploadWorkItemForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields= ['name','picture', 'classtrail_bool']

    def clean(self):
        data = self.cleaned_data
        file = data['picture']
        extension = pathlib.Path(file.name).suffix
        valid_files = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']

        if not extension.lower() in valid_files:
            raise forms.ValidationError({'picture':["File not allowed"]})
   

class CreateClasstrailForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields= ['name','picture']
     
    def clean(self):
        data = self.cleaned_data
        file = data['picture']
        extension = pathlib.Path(file.name).suffix
        valid_files = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']

        if not extension.lower() in valid_files:
            raise forms.ValidationError({'picture':["File not allowed"]})
       
class GradeWorkForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), required=False, help_text="Classroom")
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, user=None, **kwargs):
        super(GradeWorkForm, self).__init__(**kwargs)
        if user:
            self.fields['classroom'].queryset = Classroom.objects.filter(teacher_id=user)

class WorkFeedFilterForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
  

class GradeWorkUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields= ['grade']
