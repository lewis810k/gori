from rest_framework import serializers

from member.models import GoriUser
from talent.models import Registration
from .location import LocationListSerializer

__all__ = (
    'RegistrationSerializer',
)


class RegistrationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='student.name')
    talent_location = LocationListSerializer(read_only=True)
    student_level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Registration
        fields = (
            'student',
            'talent_location',
            'joined_date',
            'is_confirmed',
            'student_level',
            'experience_length',
            'message_to_tutor',
        )

    def get_student_level(self, obj):
        return obj.get_student_level_display()
