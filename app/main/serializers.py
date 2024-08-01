from rest_framework import serializers
from .models import Lecturer, LecturerSubject


class LecturerSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerSubject
        fields = ['id', 'slug']


class LecturerSerializer(serializers.ModelSerializer):
    average_ratings = serializers.IntegerField()
    subjects = LecturerSubjectSerializer(many=True)

    class Meta:
        model = Lecturer
        fields = ['id', 'first_name', 'last_name',
                  'average_ratings', 'picture', 'subjects']
