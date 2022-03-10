from types import ClassMethodDescriptorType
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from .models import User, Classroom, Teacher, Student
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import TeacherSignUpForm, StudentSignUpForm, CreateClassroomForm
from django.http import JsonResponse
# Create your views here.

def register(request):
    return render(request, '../templates/register.html')

def teacher_hub(request):
    return render(request, '../templates/teacher_hub.html')

def student_hub(request):
    return render(request, '../templates/student_hub.html')

def manage_classes(request):
    return render(request, '../templates/manage_classes.html')

def student_classes(request):
    return render(request, '../templates/student_classes.html')


class teacher_register(CreateView):
    models = User
    form_class = TeacherSignUpForm
    template_name = '../templates/teacher_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('/')

class student_register(CreateView):
    models = User
    form_class = StudentSignUpForm
    template_name = '../templates/student_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('/')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): #is_valid() checks if username and pword has the appropriate data type
            username = form.cleaned_data.get('username') #setting variables from user input
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) #authenticate checks username and password against db to check if user is valid
            if user is not None :
                login(request, user) #login() takes http request and user object to log in user
                return redirect('/')
            else:
                messages.error(request, "invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

def create_classroom(request):
    if request.POST.get('action') == 'post':
        #classroom = Classroom.objects.all()
        class_subject = request.POST.get('classroom_subject')
        class_code = request.POST.get('classroom_code')
        teacher = request.user
        classroom = Classroom(classroom_subject = class_subject, classroom_code = class_code, teacher = teacher)
        
        classroom.save()
        return JsonResponse({'status':'SUCCESS'})

def join_classroom(request):
    if request.POST.get('action') == 'post':
        #classroom = Classroom.objects.all()
        class_id = request.POST.get('classroom_id')
        print(class_id)
        user_id = request.user.id
        student = Student.objects.get(user_id = user_id)
        print(student)
        classroom = Classroom.objects.get(id = class_id)
        print(classroom)
        student.classes.add(classroom)
        student.save()
    
        return JsonResponse({'status':'SUCCESS'})




class TeacherClassesView(ListView):
    model = Classroom
    template_name = 'classroom_list.html'
    context_object_name = 'classroom_list'
    
    def get_queryset(self):
        return Classroom.objects.filter(
            teacher_id = self.request.user
        )

class StudentClassesView(ListView):
    model = Classroom
    template_name = 'student_classroom_list.html'
    context_object_name = 'classroom_list'
    
    
    def get_queryset(self):
        student_id = self.request.user.id
        print(student_id)
        return Classroom.objects.filter(
            student__user= self.request.user
        )
 


def render_classroom(request, id):
    classroom = Classroom.objects.get(id=id)
    print(classroom.id)
    return render(request, 'classroom.html', {'classroom':classroom})



class DeleteClassroomView(DeleteView):
    model = Classroom
    context_object_name = 'classroom'
    template_name = 'classroom/teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'
