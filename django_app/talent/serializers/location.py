from rest_framework import serializers

from talent.models import Talent, Location

__all__ = (
    'LocationSerializer',
    'LocationWrapperSerializers',
    'LocationListSerializer',
)


class LocationListSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.get_region_display())


class LocationSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(read_only=True)
    specific_location = serializers.SerializerMethodField(read_only=True)
    day = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Location
        fields = (
            'region',
            'specific_location',
            'registered_student',
            'day',
            'time',
            'extra_fee',
            'extra_fee_amount',
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


class LocationWrapperSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    locations = LocationSerializer(many=True)

    class Meta:
        model = Talent
        fields = (
            'id',
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
