from django.contrib import admin
from .models import Lecturer, Subject, LecturerSubject
# Register your models here.

admin.site.register(Lecturer)
admin.site.register(Subject)


@admin.register(LecturerSubject)
class LecturerSubjectAdmin(admin.ModelAdmin):
    ordering = ['subject__name']
