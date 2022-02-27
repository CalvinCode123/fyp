from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import TeacherSignUpForm, StudentSignUpForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def register(request):
    return render(request, '../templates/register.html')

def teacher_hub(request):
    return render(request, '../templates/teacher_hub.html')

def student_hub(request):
    return render(request, '../templates/student_hub.html')

def manage_classes(request):
    return render(request, '../templates/manage_classes.html')

class teacher_register(CreateView):
    models = User
    form_class = TeacherSignUpForm
    template_name = '../templates/teacher_register.html'

    @csrf_exempt
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