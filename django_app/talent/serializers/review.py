from rest_auth.app_settings import serializers
from rest_framework import serializers

from member.models import GoriUser
from talent.models import Review
from talent.models import Talent

__all__ = (
    'ReviewSerializer',
    'ReviewWrapperSerializer'
)


class ReviewSerializer(serializers.ModelSerializer):
    talent = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent.title')
    name = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='user.name')

    class Meta:
        model = Review
        fields = (
            'pk',
            'talent',
            'name',
            'curriculum',
            'readiness',
            'timeliness',
            'delivery',
            'friendliness',
            'created_date',
            'comment',
        )


class ReviewWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    reviews = ReviewSerializer(many=True)
    average_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'average_rate',
            'reviews',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()

    @staticmethod
    def get_average_rate(obj):
        sum_of_average = 0
        for review in obj.reviews.all():
            sum_of_average += review.average_rate
        return_value = sum_of_average/obj.reviews.count()
        return round(return_value, 1)
