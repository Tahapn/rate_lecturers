from django.db.models import Count
from rest_framework import serializers
from .models import Lecturer, LecturerSubject, Review


class LecturerSubjectSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    average = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = LecturerSubject
        fields = ['id', 'slug', 'average', 'ratings']

    def get_ratings(self, obj):
        return LecturerSubject.objects.values('review__rate').filter(
            lecturer=self.context['lecturer_pk'], pk=obj.pk).annotate(count=Count('review'))


class SimpleLecturerSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = LecturerSubject
        fields = ['id', 'slug',]


class LecturerSerializer(serializers.ModelSerializer):
    average_ratings = serializers.DecimalField(max_digits=3, decimal_places=2)
    subjects = SimpleLecturerSubjectSerializer(many=True)

    class Meta:
        model = Lecturer
        fields = ['id', 'first_name', 'last_name',
                  'average_ratings', 'picture', 'subjects']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'lecturer_subject', 'rate', 'comment']
        read_only_fields = ['user', 'lecturer_subject']
