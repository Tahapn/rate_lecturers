from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
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
        return LecturerSubject.objects.prefetch_related('review_set').filter(lecturer=self.kwargs['lecturer_pk']).annotate(average=Avg('review__rate'))

    def get_serializer_context(self):
        return {'lecturer_pk': self.kwargs['lecturer_pk']}


class LecturerSubjectDetail(generics.RetrieveAPIView):
    serializer_class = LecturerSubjectSerializer

    def get_object(self):
        queryset = LecturerSubject.objects.filter(
            pk=self.kwargs['pk'], lecturer=self.kwargs['lecturer_pk']).annotate(average=Avg('review__rate'))
        return get_object_or_404(queryset)

    def get_serializer_context(self):
        return {'lecturer_pk': self.kwargs['lecturer_pk']}
