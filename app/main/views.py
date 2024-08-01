from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Lecturer, LecturerSubject
from .serializers import LecturerSerializer, LecturerSubjectSerializer


def temp(request):
    return render(request, 'with_nav.html')


class LecturerViewSet(ReadOnlyModelViewSet):
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.annotate(
        average_ratings=Avg('subjects__review__rate'))


class LecturerSubjectList(generics.ListAPIView):
    serializer_class = LecturerSubjectSerializer

    def get_queryset(self, *args, **kwargs):
        return LecturerSubject.objects.filter(lecturer=self.kwargs['lecturer_pk'])


class LecturerSubjectDetail(generics.RetrieveAPIView):
    serializer_class = LecturerSubjectSerializer

    def get_object(self):
        return get_object_or_404(LecturerSubject, pk=self.kwargs['pk'], lecturer=self.kwargs['lecturer_pk'])
