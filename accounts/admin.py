from django.contrib import admin
from .models import User,Teacher,Student, Classroom, WorkItem, UserUpload
# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(WorkItem)
admin.site.register(UserUpload)