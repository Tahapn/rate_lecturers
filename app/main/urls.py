from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import temp, LecturerViewSet, LecturerSubjectList, LecturerSubjectDetail, ReviewList, ReviewDetail

router = SimpleRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns = [
    # APIs
    path('api/', include(router.urls)),
    path('api/lecturers/<int:lecturer_pk>/subjects/',
         LecturerSubjectList.as_view()),
    path('api/lecturers/<int:lecturer_pk>/subjects/<int:pk>/',
         LecturerSubjectDetail.as_view()),
    path('api/lecturers/<int:lecturer_pk>/subjects/<int:subject_pk>/comments/',
         ReviewList.as_view()),
    path('api/lecturers/<int:lecturer_pk>/subjects/<int:subject_pk>/comments/<int:pk>/',
         ReviewDetail.as_view()),

    # Templates
    path('', temp, name='home'),

]
