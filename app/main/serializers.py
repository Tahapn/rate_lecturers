from rest_framework import serializers
from .models import Lecturer


class LecturerSerializer(serializers.ModelSerializer):
    average_ratings = serializers.IntegerField()

    class Meta:
        model = Lecturer
        fields = ['id', 'first_name', 'last_name',
                  'average_ratings', 'picture']
