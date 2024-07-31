from django.shortcuts import render, HttpResponse
from django.db.models import Avg
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Lecturer
from .serializers import LecturerSerializer


def temp(request):
    return render(request, 'with_nav.html')


class LecturerViewSet(ReadOnlyModelViewSet):
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.annotate(
        average_ratings=Avg('lecturersubject__review__rate'))
