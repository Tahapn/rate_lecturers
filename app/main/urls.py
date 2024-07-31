from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import temp, LecturerViewSet

router = SimpleRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns = [
    path('', temp, name='home')
] + router.urls
