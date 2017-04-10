from django.contrib.auth import get_user_model
from rest_framework import serializers

from talent.models import Talent, Location

__all__ = (
    'LocationSerializer',
    'LocationWrapperSerializers',
    'LocationListSerializer',
    'LocationTalentSerializers',
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

    class Meta:
        model = Location
        fields = (
            'talent',
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


class LocationCreateSerializer(serializers.ModelSerializer):
    region = serializers.ChoiceField(choices=Location.REGION)
    day = serializers.ChoiceField(choices=Location.DAYS_OF_WEEK)

    class Meta:
        model = Location
        fields = (
            'talent',
            'region',
            'specific_location',
            'day',
            'extra_fee',
            'extra_fee_amount',
            'time',
        )


class LocationTalentSerializers(serializers.ModelSerializer):
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


class LocationWrapperSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'locations',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()
