from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('teacher_register/', views.teacher_register.as_view(), name='teacher_register'),
    path('student_register/', views.student_register.as_view(), name='student_register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher_hub/', views.teacher_hub, name = 'teacher_hub'),
    path('student_hub/', views.student_hub, name = 'student_hub'),
    path('manage_classes/', views.manage_classes, name = 'manage_classes'),
    path('student_classes/', views.student_classes, name = 'student_classes'),
    path('create_classroom/',views.create_classroom,name='create_classroom'),
    path('join_classroom/',views.join_classroom,name='join_classroom'),
    path('classroom_list/',views.TeacherClassesView.as_view(),name='classroom_list'),
    path('student_classroom_list/',views.StudentClassesView.as_view(),name='student_classroom_list'),
    path('classroom_list/<int:id>', views.render_classroom, name = 'classroom'),
    path('delete_classroom/<int:classroom_id>', views.delete_classroom, name = 'delete_classroom'),

    #path('classroom_list/<int:id>/delete', views.DeleteClassroomView.as_view(), name = 'classroom_delete')
]
