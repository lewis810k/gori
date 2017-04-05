import collections
from django.contrib.auth import get_user_model

from member.serializers import TutorSerializer
from talent.serializers import TalentShortInfoSerializer

from rest_framework import serializers
from talent.models import Talent, Registration
from .location import LocationListSerializer

__all__ = (
    # user
    # 'MyRegistrationSerializer',
    # 'MyRegistrationWrapperSerializer',
    # talent
    # 'TalentRegistrationSerializer',
    'TalentRegistrationWrapperSerializer',
)

User = get_user_model()


# user=================
#
# class MyRegistrationSerializer(serializers.ModelSerializer):
#     registered_talent_location = LocationListSerializer(read_only=True, source='talent_location')
#     student_level = serializers.SerializerMethodField(read_only=True)
#     talent = TalentShortInfoSerializer(source='talent_location.talent')
#     tutor_info = TutorSerializer(source='talent_location.talent.tutor', fields=('name', 'profile_image'), )
#
#     class Meta:
#         model = Registration
#         fields = (
#             'talent',
#             'registered_talent_location',
#             'is_confirmed',
#             'student_level',
#             'joined_date',
#             'experience_length',
#             'message_to_tutor',
#             'tutor_info',
#         )
#
#     def get_student_level(self, obj):
#         return obj.get_student_level_display()
#
#
# class MyRegistrationWrapperSerializer(serializers.ModelSerializer):
#     registration_info = MyRegistrationSerializer(many=True, source='registrations')
#
#     class Meta:
#         model = User
#         fields = (
#             'name',
#             'nickname',
#             'cellphone',
#             'profile_image',
#             'joined_date',
#             'registration_info',
#         )
#

# ======== talent =========
class TalentRegistrationWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    registration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'id',
            'title',
            'category',
            'type',
            'registration',
        )

    def get_registration(self, obj):
        ret = []
        for location in obj.locations.values_list('registered_student', flat=True):
            registration = Registration.objects.filter(student=location)
            sub_ret = collections.OrderedDict()
            for regi in registration:
                sub_ret["name"] = regi.student.name
                sub_ret["talent_location"] = regi.talent_location.get_region_display()
                sub_ret["student_level"] = regi.get_student_level_display()
                sub_ret["experience_length"] = regi.experience_length
                sub_ret["is_confirmed"] = regi.is_confirmed
                sub_ret["joined_date"] = regi.joined_date
                sub_ret["message_to_tutor"] = regi.message_to_tutor
                ret.append(sub_ret)
        return ret

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()


class TalentRegistrationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='student.name')
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