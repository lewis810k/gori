from rest_framework import serializers

from member.models import GoriUser
from talent.models import Registration
from talent.models import Talent
from .location import LocationSerializer

__all__ = (
    'RegistrationSerializer',
    'RegistrationWrapperSerializers'
)


class RegistrationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='student.name')
    # talent_location = LocationListSerializer(read_only=True)
    student_level = serializers.SerializerMethodField(read_only=True)
    talent_location = LocationSerializer(read_only=True)

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


class RegistrationWrapperSerializers(serializers.ModelSerializer):
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
            sub_ret = {}
            for regi in registration:
                sub_ret["student"]=regi.student.name
                sub_ret["talent_location"] =regi.talent_location.get_region_display()
                sub_ret["joined_date"]=regi.joined_date
                sub_ret["is_confirmed"]=regi.is_confirmed
                sub_ret["student_level"]=regi.get_student_level_display()
                sub_ret["experience_length"]=regi.experience_length
                sub_ret["message_to_tutor"]=regi.message_to_tutor
                ret.append(sub_ret)
        # for registration_student in obj.locations.values_list('registered_student', flat=True):
        #     print(registration_student)
        #     registration = Registration.objects.filter(talent_location=registration_student)
        #     print(registration)
        #     for regi in registration:
        #         if regi.talent_location.talent.id == obj.id:
        #             student.append(regi.student.name)
        return ret

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()

        # @staticmethod
        # def get_id(obj):
        #     return obj.talent_location.talent.id
