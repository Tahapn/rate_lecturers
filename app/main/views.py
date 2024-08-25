from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Lecturer, LecturerSubject, Review
from .serializers import LecturerSerializer, LecturerSubjectSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from .forms import ReviewForm

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

    lecturer_subject = get_object_or_404(
        LecturerSubject, lecturer__slug=lecturer_slug, subject__slug=subject_slug)

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['rate'] = int(post_data['rate'])
        form = ReviewForm(post_data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.lecturer_subject = lecturer_subject
            instance.save()
            return HttpResponseRedirect(request.get_full_path())

    else:
        form = ReviewForm()

        lecturer = get_object_or_404(
            Lecturer.objects.filter(slug=lecturer_slug).annotate(
                average=Round(Avg('subjects__review__rate'), 2)
            )
        )

        lecturer = Lecturer.objects.annotate(
            average=Round(Avg('subjects__review__rate'), 2)
        ).get(slug=lecturer_slug)

        queryset = Review.objects.filter(
            lecturer_subject=lecturer_subject)

        user_review = queryset.filter(user=request.user).first(
        ) if request.user.is_authenticated else None

        ratings_count = LecturerSubject.objects.values('review__rate').filter(
            lecturer__slug=lecturer_slug, subject__slug=subject_slug).annotate(count=Count('review')).order_by('-review__rate')

        return render(request, 'main/subject.html', {'reviews': queryset, 'lecturer': lecturer, 'ratings': ratings_count, 'form': form, 'user_review': user_review})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user:
        msg = ["You don't have permission to access this url"]
        return render(request, 'redirect.html', {'messages': msg})
    elif request.method == 'POST':
        form = ReviewForm(instance=review, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)
        return render(request, 'main/edit_review.html', {'form': form})
