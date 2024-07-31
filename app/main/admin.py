from django.contrib import admin
from .models import Lecturer, Subject, LecturerSubject, Review
# Register your models here.

admin.site.register(Lecturer)
admin.site.register(Subject)


@admin.register(LecturerSubject)
class LecturerSubjectAdmin(admin.ModelAdmin):
    ordering = ['subject__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'lecturer_subject']
