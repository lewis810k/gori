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
    user = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='user.name')
    class Meta:
        model = Review
        fields = (
            'talent',
            'user',
            'created_date',
            'curriculum_rate',
            'readiness_rate',
            'timeliness_rate',
            'delivery_rate',
            'friendliness_rate'
        )

class ReviewWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Talent
        fields = (
            'id',
            'title',
            'category',
            'type',
            'reviews',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()