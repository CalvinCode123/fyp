#Imports
from types import ClassMethodDescriptorType
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, DetailView, FormView, UpdateView
from .models import User, Classroom, Teacher, Student, UserUpload, WorkItem
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import JoinClassroomForm, TeacherSignUpForm, StudentSignUpForm, CreateClassroomForm, CreateWorkItemForm, CreateClasstrailForm, UploadWorkItemForm, GradeWorkForm, WorkFeedFilterForm, GradeWorkUploadForm
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

#FBV to load static pages
def register(request):
    return render(request, '../templates/register.html')

def teacher_hub(request):
    if request.user.is_authenticated and request.user.is_teacher:
        return render(request, '../templates/teacher_hub.html')
    else:
        raise PermissionDenied()
def student_hub(request):
    if request.user.is_authenticated and request.user.is_student:
        return render(request, '../templates/student_hub.html')
    else:
        raise PermissionDenied()

def manage_classes(request):
    return render(request, '../templates/manage_classes.html')

#CBV CreateView render usercreationform in template, then create teacher object.
class teacher_register(CreateView):
    models = User
    form_class = TeacherSignUpForm #form defined in forms.py
    template_name = '../templates/teacher_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('/')

#CBV CreateView render usercreationform in template, then create student object.
class student_register(CreateView):
    models = User
    form_class = StudentSignUpForm
    template_name = '../templates/student_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('/')

#login method, 
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
        
        else:
            messages.error(request, "invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

#logout mehtod
def logout_view(request):
    logout(request)
    return redirect('/')

#create classroom view
class CreateClassroomView(CreateView):
    #renders form
    def get(self, request, *args, **kwargs):
        context = {'form': CreateClassroomForm()}
        return render(request, '../templates/manage_classes.html', context)

    #posts form
    def post(self, request, *args, **kwargs):
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit = False)
            classroom.teacher = self.request.user
            classroom.save()
            messages.success(request, 'Classroom: '+ classroom.classroom_subject + ' created succesfully')
            return redirect('classroom_list')
        else:
            return render(request, '../templates/manage_classes.html', {'form': form})

#method to join classroom
class JoinClassView(SuccessMessageMixin, FormView):
    template_name = 'join_classroom.html'
    form_class = JoinClassroomForm
    success_url = '../student_classroom_list/'
    success_message = 'Successfully joined classroom'
   
    def form_valid(self, form):
        id = form.cleaned_data['classroom_id']
        code = form.cleaned_data['classroom_code']

        user_id = self.request.user
        student = Student.objects.get(user_id = user_id)
        
        classroom = Classroom.objects.get(id = id)

        if classroom.classroom_code == code: #checking that classroom code matches
            student.classes.add(classroom)
            student.save()   
        
        return super().form_valid(form)
        


        
#listview for teacher viewing classrooms
class TeacherClassesView(ListView):
    model = Classroom
    template_name = 'classroom_list.html'
    context_object_name = 'classroom_list'
    
    def get_queryset(self):
        return Classroom.objects.filter(
            teacher_id = self.request.user
        )

#listview for students viewing classrooms
class StudentClassesView(UserPassesTestMixin,ListView):
    model = Classroom
    template_name = 'student_classroom_list.html'
    context_object_name = 'classroom_list'

    #restricts view to only students
    def test_func(self):
        return self.request.user.is_student
    
    #get_queryset returns a queryset of objects. This queryset gets all the classrooms, where the student is enrolled.
    def get_queryset(self):
        return Classroom.objects.filter(
            student__user= self.request.user
        )
 
class ViewGradesView(UserPassesTestMixin,ListView):
    model = WorkItem
    template_name = 'view_grades.html'
    context_object_name = 'work_list'

    def test_func(self):
        return self.request.user.is_student

    def get_queryset(self):
        return Classroom.objects.filter(student__user= self.request.user)


class RendClassroom(DetailView):
    model = Classroom
    template_name = 'classroom.html'


    def delete(request, id):
        print(id)
        deleted_room = Classroom.objects.get(id=id)
        Classroom.objects.filter(id=id).delete()
        
        messages.error(request, 'Successfully deleted classroom: ' + deleted_room.classroom_subject)
        return redirect('classroom_list')



class DeleteClassroomView(DeleteView):
    model = Classroom
    success_url = "/"



class CreateWorkView(CreateView):
        
    def get(self, request, *args, **kwargs):
        context = {'form': CreateWorkItemForm(user = request.user)}
        return render(request, '../templates/assign_work.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateWorkItemForm(user=request.user,data = request.POST)
        if form.is_valid():
            work_item = form.save(commit = False)
            today = date.today()
            print("today:")   
            print(today)

            if WorkItem.objects.filter(classroom = work_item.classroom, date_assigned = today):
                messages.error(request, 'work already created for today')
            else:
                print(work_item)
                work_item.save()
                #return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
                messages.success(request, 'Succesfully created work')
            return render(request, 'assign_work.html', {'form': form})

class WorkFeedView(UserPassesTestMixin,ListView):
    model = Classroom
    template_name = 'work_feed.html'
    context_object_name = 'work_list'

    def test_func(self):
        return self.request.user.is_student


    def get_queryset(self):
        self.form = WorkFeedFilterForm(data = self.request.GET or None)

        if self.request.GET and self.form.is_valid():
            date = self.form.cleaned_data.get("date")
            print(date)

            return WorkItem.objects.filter(
                classroom__student__user=self.request.user
            ).filter(
                date_assigned = date
            )
        else:

            return WorkItem.objects.filter(
                classroom__student__user=self.request.user
            ).order_by(
                '-date_assigned'
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # this calls self.get_queryset() which assigns self.form
        context['form'] = self.form
        return context

class TeacherWorkFeedView(ListView):
    model = Classroom
    template_name = 'teacher_work_feed.html'
    context_object_name = 'work_list'


    def get_queryset(self):
        self.form = WorkFeedFilterForm(data = self.request.GET or None)

        if self.request.GET and self.form.is_valid():
            date = self.form.cleaned_data.get("date")
            print(date)

            return WorkItem.objects.filter(
                classroom__teacher=self.request.user
            ).filter(
                date_assigned = date
            )
        else:
            
            return WorkItem.objects.filter(
                classroom__teacher=self.request.user
            ).order_by(
                '-date_assigned'
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # this calls self.get_queryset() which assigns self.form
        context['form'] = self.form
        return context



class EditWorkView(SuccessMessageMixin, UpdateView):
    model = WorkItem
    template_name = 'edit_work_detail.html'
    success_message = 'Work description sucessfully updated.'
    fields = ["work_description"]

    def get_success_url(self):
        return reverse_lazy('edit_work', kwargs={'pk': self.object.id})    

class WorkFeedUploadView(UserPassesTestMixin,CreateView):

    def test_func(self):
        return self.request.user.is_student

    def get(self, request, *args, **kwargs):
        context = {'form': UploadWorkItemForm()}
        return render(request, '../templates/upload_work.html', context)

    def post(self, request, *args, **kwargs):
        form = UploadWorkItemForm(request.POST, request.FILES)
        x = self.kwargs.get('id')
        print(x)
        if form.is_valid():
            upload_item = form.save(commit = False)
            today = date.today()
            upload_item.date = today
            upload_item.student_id = self.request.user.id
            upload_item.submission = WorkItem.objects.get(id = x)
            if UserUpload.objects.filter(submission =  x):
                print("already uploaded")
                messages.error(request, 'Work already submitted for this assignment')

            else:  
                upload_item.save()
                messages.success(request, 'Item sucessfully uploaded')
            return redirect('work_feed')
        else: 
            print("form not valid")
            return render(request, '../templates/upload_work.html', {'form': form})


 

class ClassTrail(UserPassesTestMixin, ListView):
    model = UserUpload
    template_name = 'classtrail.html'
    context_object_name = 'classtrail_list'
    paginate_by = 4

    def test_func(self):
        return self.request.user.is_student
    
    def get_queryset(self):
        student_id = self.request.user.id
        print(student_id)

        return UserUpload.objects.filter(
            student_id= self.request.user
        ).filter(
            classtrail_bool = True
        ).order_by('-date')


class CreateClassTrailView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': CreateClasstrailForm()}
        return render(request, '../templates/add_classtrail.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateClasstrailForm(request.POST, request.FILES)
        print("hello")
        if form.is_valid():
            ct_item = form.save(commit = False)
            print("hello")
            today = date.today()
            ct_item.date = today
            ct_item.student_id = self.request.user.id
            ct_item.save()
            messages.success(request, 'Successfully added item:  '+ ct_item.name)
            return redirect('classtrail')
            #return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
        else:
            return render(request, '../templates/add_classtrail.html', {'form': form})


    
 
class ClassTrailDetailView(DetailView):
    model = UserUpload
    template_name = 'userupload_detail.html'

    def test_func(self):
        return self.request.user.is_student

    def delete(request, pk):
        print(id)
        deleted_item = UserUpload.objects.get(pk=pk)
        UserUpload.objects.filter(pk=pk).delete()
        
        messages.success(request, 'Successfully deleted item: ' + deleted_item.name)
        return redirect('classtrail')


class GradeWorkUploadView(SuccessMessageMixin, UpdateView):
    model = UserUpload
    template_name = 'grade_work_upload_detail.html'

    fields = ["grade"]

    success_message = 'Grade Submitted'

    def get_success_url(self):
        return reverse_lazy('grade_work_item', kwargs={'pk': self.object.id})


class GradeWorkDetailView(ListView):
    model = UserUpload
    template_name = 'grade_work.html'
    context_object_name = 'work_list'

    def get_queryset(self):
        self.form = GradeWorkForm(data = self.request.GET or None, user = self.request.user)
        if self.request.GET and self.form.is_valid():
            room = self.form.cleaned_data.get("classroom") 
            date = self.form.cleaned_data.get("date")


            all_students = Student.objects.filter(classes = room.id)
            print(all_students)
           
            submitted = UserUpload.objects.filter(date = date).filter(submission__classroom = room.id)
            print("submitted:")
            print(submitted)
            filtstud =Student.objects.filter(classes = room.id)
            
            workd = WorkItem.objects.filter(date_assigned = date).filter(classroom_id = room.id)
            
            workd = workd.first()

            if workd == None:
                print("no work")
                queryset = {
                }
                return queryset
            else:
                queryset = {
                    'workdesc': WorkItem.objects.filter(date_assigned = date).filter(classroom = room),
                    'not_submitted': Student.objects.filter(classes = room.id).exclude(user__in= UserUpload.objects.filter(submission_id = workd).filter(submission__classroom = room.id).values_list('student')), 
                    'submitted': UserUpload.objects.filter(submission__classroom = room.id).filter(submission_id = workd)
                }
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # this calls self.get_queryset() which assigns self.form
        context['form'] = self.form
        return context