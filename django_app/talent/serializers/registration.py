import collections

from django.contrib.auth import get_user_model
from rest_framework import serializers

from member.serializers import TutorSerializer
from talent.models import Talent, Registration, Location
from talent.serializers import TalentShortInfoSerializer
from .location import LocationListSerializer

__all__ = (
    # user
    'MyRegistrationSerializer',
    'MyRegistrationWrapperSerializer',
    # talent
    # 'TalentRegistrationSerializer',
    'TalentRegistrationWrapperSerializer',
)

User = get_user_model()


# user=================
class MyRegistrationSerializer(serializers.ModelSerializer):
    registered_location = LocationListSerializer(read_only=True, source='talent_location')
    student_level = serializers.SerializerMethodField(read_only=True)
    talent = TalentShortInfoSerializer(source='talent_location.talent')
    tutor_info = TutorSerializer(source='talent_location.talent.tutor',
                                 fields=('pk', 'user_id', 'name', 'profile_image'), )

    class Meta:
        model = Registration
        fields = (
            'pk',
            'registered_location',
            'is_verified',
            'student_level',
            'joined_date',
            'experience_length',
            'message_to_tutor',
            'talent',
            'tutor_info',
        )

    def get_student_level(self, obj):
        return obj.get_student_level_display()


class MyRegistrationWrapperSerializer(serializers.ModelSerializer):
    results = MyRegistrationSerializer(many=True,source="registrations")
    user_id = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = (
            'pk',
            'user_id',
            'name',
            'nickname',
            'cellphone',
            'profile_image',
            'joined_date',
            'results',
        )


# ======== talent =========
class TalentRegistrationWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    registrations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'registrations',
        )

    @staticmethod
    def get_registrations(obj):
        registrations = []
        # test, test2 = obj.locations.values_list('registered_student', 'id')
        for location in obj.locations.values_list('registered_student', 'id'):
            if None not in location and location not in registrations:
                registrations.append(location)
        # print(registrations)

        ret = []
        for student_id, location_id in registrations:
            registration = Registration.objects.filter(student_id=student_id, talent_location_id=location_id).first()
            sub_ret = collections.OrderedDict()
            sub_ret["pk"] = registration.id
            sub_ret["name"] = registration.student.name
            sub_ret["talent_location"] = registration.talent_location.get_region_display()
            sub_ret["student_level"] = registration.get_student_level_display()
            sub_ret["experience_length"] = registration.experience_length
            sub_ret["is_verified"] = registration.is_verified
            sub_ret["joined_date"] = registration.joined_date
            sub_ret["message_to_tutor"] = registration.message_to_tutor
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
    day = serializers.SerializerMethodField()
    student_level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Registration
        fields = (
            'id',
            'student',
            'talent_location',
            'day',
            'is_verified',
            'student_level',
            'experience_length',
            'joined_date',
            'message_to_tutor',
        )

    def get_student_level(self, obj):
        print(dir(obj))
        return obj.get_student_level_display()

    def get_day(self, obj):
        return obj.talent_location.get_day_display()


class TalentRegistrationCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='student')
    location_pk = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source='talent_location')

    class Meta:
        model = Registration
        fields = (
            'id',
            'user',
            'location_pk',
            'student_level',
            'experience_length',
            'message_to_tutor',
        )