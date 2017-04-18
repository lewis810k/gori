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
    'MyApplicantsSerializer',
    'MyRegistrationWrapperSerializer',
    'MyEnrolledTalentWrapperSerializer',
    'MyPageAllSerializer',
    'MyPageWrapperSerializer',
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
    # results = MyRegistrationSerializer(many=True, source="registrations")
    results = serializers.SerializerMethodField()
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

    def get_results(self, obj):
        if obj.registrations.all().filter(is_verified=False):
            return MyRegistrationSerializer(obj.registrations.all().filter(is_verified=False), many=True).data
        else:
            return []


class MyEnrolledTalentWrapperSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
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

    def get_results(self, obj):
        if obj.registrations.all().filter(is_verified=True):
            return MyRegistrationSerializer(obj.registrations.all().filter(is_verified=True), many=True).data
        else:
            print(obj.registrations.all().filter(is_verified=True))
            return []


# tutor의 수업에 대한 수강신청서
class MyApplicantsSerializer(serializers.ModelSerializer):
    registered_location = LocationListSerializer(read_only=True, source='talent_location')
    student_level = serializers.SerializerMethodField(read_only=True)
    talent = TalentShortInfoSerializer(source='talent_location.talent')

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
        )

    def get_student_level(self, obj):
        return obj.get_student_level_display()


# MyPage에 들어가는 모든 Serializer를 불러오는 serializer
class MyPageWrapperSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
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

    def get_results(self, obj):
        return MyPageAllSerializer(obj).data


class MyPageAllSerializer(serializers.ModelSerializer):
    wishlist = serializers.SerializerMethodField()
    registrations = serializers.SerializerMethodField()
    enrollment = serializers.SerializerMethodField()
    talents = serializers.SerializerMethodField()
    applicants = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'wishlist',
            'registrations',
            'enrollment',
            'talents',
            'applicants',

        )

    def get_wishlist(self, obj):
        return TalentShortInfoSerializer(obj.talent_set.all(), many=True).data

    def get_registrations(self, obj):
        if obj.registrations.all().filter(is_verified=False):
            return MyRegistrationSerializer(obj.registrations.all().filter(is_verified=False), many=True).data
        else:
            return []

    def get_enrollment(self, obj):
        if obj.registrations.all().filter(is_verified=False):
            return MyRegistrationSerializer(obj.registrations.all().filter(is_verified=True), many=True).data
        else:
            return []

    def get_talents(self, obj):
        talents = Talent.objects.filter(tutor__user=obj)
        return TalentShortInfoSerializer(talents.all(), many=True).data

    def get_applicants(self, obj):
        user = obj
        if hasattr(user, "tutor"):
            registrations = []
            for talent in user.tutor.talent_set.all():
                registrations.extend([item for item in Registration.objects.filter(talent_location__talent=talent)])
                return MyApplicantsSerializer(registrations, many=True).data
        else:
            return []


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
