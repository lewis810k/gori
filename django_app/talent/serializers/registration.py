from rest_framework import serializers

from member.serializers import TutorSerializer
from member.tests import User
from talent.models import Registration
from talent.serializers import TalentShortInfoSerializer
from .location import LocationListSerializer

__all__ = (
    'RegistrationSerializer',
    'MyRegistrationListSerializer',
)


class RegistrationSerializer(serializers.ModelSerializer):
    registered_talent_location = LocationListSerializer(read_only=True, source='talent_location')
    student_level = serializers.SerializerMethodField(read_only=True)
    talent = TalentShortInfoSerializer(source='talent_location.talent')
    tutor_info = TutorSerializer(source='talent_location.talent.tutor', fields=('name','profile_image'), )

    class Meta:
        model = Registration
        fields = (
            'talent',
            'registered_talent_location',
            'is_confirmed',
            'student_level',
            'joined_date',
            'experience_length',
            'message_to_tutor',
            'tutor_info',
        )

    def get_student_level(self, obj):
        return obj.get_student_level_display()


class MyRegistrationListSerializer(serializers.ModelSerializer):
    registration_info = RegistrationSerializer(many=True, source='registrations')

    class Meta:
        model = User
        fields = (
            'name',
            'nickname',
            'cellphone',
            'profile_image',
            'joined_date',
            'registration_info',
        )
