from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Avg, Count
from django.db.models.functions import Round
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Lecturer, LecturerSubject, Review
from .serializers import LecturerSerializer, LecturerSubjectSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly


#### APIs ####


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


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(lecturer_subject=self.kwargs['subject_pk'])

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user, lecturer_subject_id=self.kwargs['subject_pk'])


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(lecturer_subject_id=self.kwargs['subject_pk'], pk=self.kwargs['pk'])

#### Templates ####


def home(request):
    lecturers = Lecturer.objects.prefetch_related('subjects__subject').annotate(
        average_ratings=Round(Avg('subjects__review__rate'), 2)
    )

    return render(request, 'main/home.html', {'lecturers': lecturers})


def subjects(request, lecturer_slug, subject_slug):

    lecturer = get_object_or_404(
        Lecturer.objects.filter(slug=lecturer_slug).annotate(
            average=Round(Avg('subjects__review__rate'), 2)
        )
    )

    ratings_count = LecturerSubject.objects.values('review__rate').filter(
        lecturer__slug=lecturer_slug, subject__slug=subject_slug).annotate(count=Count('review')).order_by('-review__rate')

    queryset = Review.objects.filter(
        lecturer_subject__lecturer__slug=lecturer_slug, lecturer_subject__subject__slug=subject_slug)
    return render(request, 'main/subject.html', {'reviews': queryset, 'lecturer': lecturer, 'ratings': ratings_count})
