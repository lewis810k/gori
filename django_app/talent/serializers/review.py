from rest_auth.app_settings import serializers
from rest_framework import serializers

from member.serializers.user import ReviewUserSerializer
from talent.models import Review
from talent.models import Talent
from utils import review_average_rate, curriculum_average_rate, timeliness_average_rate, delivery_average_rate, \
    friendliness_average_rate, readiness_average_rate

__all__ = (
    'ReviewSerializer',
    'ReviewWrapperSerializer'
)


class ReviewSerializer(serializers.ModelSerializer):
    talent = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent.title')
    # name = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='user.name')
    user = ReviewUserSerializer()

    class Meta:
        model = Review
        fields = (
            'pk',
            'talent',
            'user',
            'curriculum',
            'readiness',
            'timeliness',
            'delivery',
            'friendliness',
            'created_date',
            'comment',
        )


class AverageRatesSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(read_only=True)
    curriculum = serializers.SerializerMethodField(read_only=True)
    timeliness = serializers.SerializerMethodField(read_only=True)
    readiness = serializers.SerializerMethodField(read_only=True)
    delivery = serializers.SerializerMethodField(read_only=True)
    friendliness = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'total',
            'curriculum',
            'readiness',
            'timeliness',
            'delivery',
            'friendliness',

        )

    @staticmethod
    def get_total(obj):
        return review_average_rate(obj.reviews)

    @staticmethod
    def get_curriculum(obj):
        return curriculum_average_rate(obj.reviews)

    @staticmethod
    def get_timeliness(obj):
        return timeliness_average_rate(obj.reviews)

    @staticmethod
    def get_friendliness(obj):
        return friendliness_average_rate(obj.reviews)

    @staticmethod
    def get_delivery(obj):
        return delivery_average_rate(obj.reviews)

    @staticmethod
    def get_readiness(obj):
        return readiness_average_rate(obj.reviews)


class ReviewWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    reviews = ReviewSerializer(many=True)
    average_rates = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'average_rates',
            'review_count',
            'reviews',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()

    @staticmethod
    def get_average_rates(obj):
        return AverageRatesSerializer(obj).data

    @staticmethod
    def get_review_count(obj):
        return obj.reviews.count()
