from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import temp, LecturerViewSet, LecturerSubjectList, LecturerSubjectDetail

router = SimpleRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns = [
    # APIs
    path('api/', include(router.urls)),
    path('api/lecturers/<int:lecturer_pk>/subjects/',
         LecturerSubjectList.as_view()),
    path('api/lecturers/<int:lecturer_pk>/subjects/<int:pk>/',
         LecturerSubjectDetail.as_view()),

    # Templates
    path('', temp, name='home'),

]
