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
    path('create_classroom/',views.create_classroom,name='create_classroom'),
    path('classroom_list/',views.TeacherClassesView.as_view(),name='classroom_list'),
    path('classroom_list/<int:id>', views.render_classroom, name = 'classroom')
]
