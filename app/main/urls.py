from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import home, subjects, LecturerViewSet, LecturerSubjectList, LecturerSubjectDetail, ReviewList, ReviewDetail

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
    path('', home, name='home'),
    path('ratings/<str:lecturer_slug>/<str:subject_slug>/',
         subjects, name='subjects')
]
