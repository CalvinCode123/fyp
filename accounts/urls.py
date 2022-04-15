from django.urls import path
from . import views

#urls and thier paths, first argument is the url, second argument is the method or view, the third argument is the name of the template tag.
urlpatterns=[
    path('register/', views.register, name='register'),
    path('teacher_register/', views.teacher_register.as_view(), name='teacher_register'),
    path('student_register/', views.student_register.as_view(), name='student_register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher_hub/', views.teacher_hub, name = 'teacher_hub'),
    path('student_hub/', views.student_hub, name = 'student_hub'),
    path('manage_classes/', views.CreateClassroomView.as_view(), name = 'manage_classes'),
    path('join_class/',views.JoinClassView.as_view(),name='join_classroom'),
    path('classroom_list/',views.TeacherClassesView.as_view(),name='classroom_list'),
    path('student_classroom_list/',views.StudentClassesView.as_view(),name='student_classroom_list'),
    path('classroom_list/<pk>/', views.RendClassroom.as_view(), name='classroom'),
    path('classroom_list/<int:id>/delete', views.RendClassroom.delete, name = 'delete_classroom'),
    path('assign_work/', views.CreateWorkView.as_view(), name='assign_work'),
    path('work_feed/',views.WorkFeedView.as_view(),name='work_feed'),
    path('teacher_work_feed/',views.TeacherWorkFeedView.as_view(),name='teacher_work_feed'),
    path('edit_work/<pk>/',views.EditWorkView.as_view(), name = 'edit_work'),
    path('work_feed/upload/<int:id>',views.WorkFeedUploadView.as_view(),name='work_upload'),
    path('work_feed/',views.WorkFeedView.as_view(),name='work_feed_date'),
    path('classtrail/',views.ClassTrail.as_view(),name='classtrail'),
    path('classtrail/add/', views.CreateClassTrailView.as_view(), name='classtrail_add'),
    path('classtrail/<pk>/delete', views.ClassTrailDetailView.delete, name = 'delete_classtrail_item'),
    path('classtrail/<pk>/',views.ClassTrailDetailView.as_view(), name = 'classtrail_item'), #<pk> is the primary key and used to view a single object from the listview
    path('grade_work/', views.GradeWorkDetailView.as_view(), name='grade_work'),
    path('grade_work/<pk>/',views.GradeWorkUploadView.as_view(), name = 'grade_work_item'),
    path('view_grades/',views.ViewGradesView.as_view(),name='view_grades'),
]
