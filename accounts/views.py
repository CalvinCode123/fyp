from types import ClassMethodDescriptorType
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, DetailView, FormView, UpdateView
from .models import User, Classroom, Teacher, Student, UserUpload, WorkItem
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import TeacherSignUpForm, StudentSignUpForm, CreateClassroomForm, CreateWorkItemForm, CreateClasstrailForm, UploadWorkItemForm, GradeWorkForm, WorkFeedFilterForm, GradeWorkUploadForm
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.
from django.core.exceptions import PermissionDenied

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
        
        else:
            messages.error(request, "invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

'''
def create_classroom(request):
    if request.POST.get('action') == 'post':
        #classroom = Classroom.objects.all()
        class_subject = request.POST.get('classroom_subject')
        class_code = request.POST.get('classroom_code')
        teacher = request.user
        classroom = Classroom(classroom_subject = class_subject, classroom_code = class_code, teacher = teacher)
        
        classroom.save()
        messages.success(request, "joined class")
    
    #return render(request, '../templates/manage_classes.html')
    return redirect('classroom_list')
        #return JsonResponse({'status':'SUCCESS'})
'''

class CreateClassroomView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': CreateClassroomForm()}
        return render(request, '../templates/manage_classes.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit = False)
            classroom.teacher = self.request.user
            classroom.save()
            #return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))

        else:
            print("form not valid")

        messages.success(request, 'Classroom: '+ classroom.classroom_subject + ' created succesfully')
        return redirect('classroom_list')


'''
def create_classroom(request):
    if request.method=='POST':
        form = CreateClassroomForm(data=request.POST)
        if form.is_valid(): #is_valid() checks if username and pword has the appropriate data type
            class_subject = form.cleaned_data.get('classroom_subject') #setting variables from user input
            class_code = form.cleaned_data.get('classroom_code')
            teacher = request.user
            classroom = Classroom(classroom_subject = class_subject, classroom_code = class_code, teacher = teacher)
            classroom.save()
            messages.success(request, "classroom successfully created")

        else:
            messages.error(request, "")
    return render(request, '../templates/manage_classes',
    context={'form':CreateClassroomForm()})
'''

def join_classroom(request):
    if request.POST.get('action') == 'post':
        #classroom = Classroom.objects.all()
        class_id = request.POST.get('classroom_id')
        class_code = request.POST.get('classroom_code')
        print(class_id)
        user_id = request.user.id
        student = Student.objects.get(user_id = user_id)
        print(student)
        classroom = Classroom.objects.get(id = class_id)
        print(classroom)
        if classroom.classroom_code == class_code:
            student.classes.add(classroom)
            student.save()     
            messages.success(request, 'Succesfully joined class')
            return redirect('student_classroom_list')

        else:
            messages.error(request, "invalid classroom id or code")
            return redirect('student_classroom_list')

        return HttpResponseRedirect('/student_classroom_list/')


 



class TeacherClassesView(ListView):
    model = Classroom
    template_name = 'classroom_list.html'
    context_object_name = 'classroom_list'
    
    def get_queryset(self):
        return Classroom.objects.filter(
            teacher_id = self.request.user
        )


class StudentClassesView(UserPassesTestMixin,ListView):
    model = Classroom
    template_name = 'student_classroom_list.html'
    context_object_name = 'classroom_list'

    def test_func(self):
        return self.request.user.is_student
    
    
    def get_queryset(self):
        student_id = self.request.user.id
        print(student_id)
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

'''
class WorkFeedView(ListView):
    model = Classroom
    template_name = 'work_feed.html'
    context_object_name = 'work_list'
    
    def get_queryset(self):
        student_id = self.request.user.id

        today = date.today()
        print("todays date:")
        print(today)
        
        if 'date' in self.kwargs:

            urlval = self.kwargs.get('date')
            urlval = datetime.strptime(urlval, "%Y-%m-%d").date()
            print("url's date:")
            print(urlval)

            work_today = WorkItem.objects.filter(
                date_assigned = urlval
            )

            x = WorkItem.objects.filter(
                classroom__student__user=self.request.user
            ).filter(
                date_assigned = urlval
            )

            print("x is:")
            print(x)
            print("dates work")
            print(work_today)




            return x
        else:
            x = WorkItem.objects.filter(
                classroom__student__user=self.request.user
            ).filter(
                date_assigned = today
            )
            return x
        
 '''       
'''
        Classroom.objects.filter(
            student__user= self.request.user
        ).exclude(
            workitem__isnull=True
        )
'''
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
            upload_item.save()
            #return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))

        else:
            print("form not valid")

        messages.success(request, 'Item sucessfully added to classtrail')
        return redirect('classtrail')

 

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

    def test_func(self):
        return self.request.user.is_student

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
            ct_item.time = today
            ct_item.student_id = self.request.user.id
            ct_item.save()
            #return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
        else:
            print("form not valid")
        messages.success(request, 'Successfully added item:  '+ ct_item.name)
        return redirect('classtrail')

    
 
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

'''
class GradeWorkUploadView(DetailView):
    model = UserUpload
    template_name = 'grade_work_upload_detail.html'

    def get_context_data(self, **kwargs):
          context = super(GradeWorkUploadView, self).get_context_data(**kwargs)
          context['GradeWorkUploadView'] = GradeWorkUploadForm()
          return context

    def post(self, request, *args, **kwargs):
          
          form = GradeWorkUploadForm(request.POST)

          if form.is_valid():
             # from here you need to change your post request according to your requirement, this is just a demo
             obj  = form.save(commit=False)
             print(obj)
             return redirect('grade_work_item', id) #add your url
'''

class GradeWorkUploadView(SuccessMessageMixin, UpdateView):
    model = UserUpload
    template_name = 'grade_work_upload_detail.html'

    fields = ["grade"]

    success_message = 'Grade Submitted'

    def get_success_url(self):
        return reverse_lazy('grade_work_item', kwargs={'pk': self.object.id})

    

'''
    def grade(request, id):
        print(id)
        upload = UserUpload.objects.get(id=id)
        if request.POST.get('action') == 'post':
        #classroom = Classroom.objects.all()
            grade = request.POST.get('grade')
            upload.grade = grade
            upload.save()
            messages.success(request, 'Grade Submitted ')
            return redirect('grade_work_item')
'''
    

'''
        classrooms = Classroom.objects.filter(
            student__user= self.request.user
        )    
        
        work = []
        for room in classrooms:
            for x in room.workitem_set.all():
                work.append(x)
        print(work)
        work
        return work
'''     

'''
class GradeWorkView(FormView):
    template_name = 'grade_work.html'
    form_class = GradeWorkForm
    success_url = '/#'
    context_object_name = 'work_list'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        data= form.cleaned_data.get("classroom") 
        data= form.cleaned_data.get("date")
        print(data)
        return super().form_valid(form)  
'''

'''
class GradeWorkDetailView(ListView, FormMixin):
    model = UserUpload
    form_class = GradeWorkForm
    template_name = 'grade_work.html'
    context_object_name = 'work_list'

    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.form_class)
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            classroom = request.POST.get('classroom')
            date = request.POST.get('date')
 
        
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # Just include the form
        context = super(GradeWorkDetailView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        return context

    def get_queryset(self):

        return UserUpload.objects.all()
'''

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