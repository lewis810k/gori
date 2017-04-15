from django.contrib.auth import get_user_model
from rest_framework import serializers

from talent.models import Talent, Location

__all__ = (
    'LocationSerializer',
    'LocationListSerializer',
    'LocationTalentSerializer',
    'LocationCreateSerializer',
)

User = get_user_model()


class LocationListSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.get_region_display())


class LocationSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    specific_location = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    # registered_student = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField()
    talent_pk = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.id')

    class Meta:
        model = Location
        fields = (
            'pk',
            'talent_pk',
            'region',
            'specific_location',
            # 'registered_student',
            'day',
            'extra_fee',
            'extra_fee_amount',
            'time',
        )

    @staticmethod
    def get_region(obj):
        return obj.get_region_display()

    @staticmethod
    def get_specific_location(obj):
        return obj.get_specific_location_display()

    @staticmethod
    def get_day(obj):
        return obj.get_day_display()

    @staticmethod
    def get_time(obj):
        return obj.time_list

        # @staticmethod
        # def get_registered_student(obj):
        #     # print(obj.registered_student)
        #     print(obj.registered_student.values_list('name'))
        #     return obj.registered_student_display()


class LocationTalentSerializer(serializers.ModelSerializer):
    talent_title = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.title')
    talent_id = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.id')
    talent_category = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.category')
    talent_type = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.type')

    class Meta:
        model = Location
        fields = (
            'talent_id'
            'talent_title'
            'talent_category'
            'talent_type'

        )


class LocationCreateSerializer(serializers.ModelSerializer):
    talent_pk = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent')

    class Meta:
        model = Location
        fields = (
            'talent_pk',
            'region',
            'specific_location',
            'location_info',
            'extra_fee',
            'extra_fee_amount',
            'day',
            'time',
        )
