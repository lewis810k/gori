from django.contrib.auth import get_user_model
from rest_framework import serializers

from talent.serializers import TalentShortInfoSerializer

User = get_user_model()

__all__ = (
    'MyWishListSerializer',
)


class MyWishListSerializer(serializers.ModelSerializer):
    talent = TalentShortInfoSerializer(many=True, source='talent_set')

    class Meta:
        model = User
        fields = (
            'name',
            'nickname',
            'cellphone',
            'profile_image',
            'joined_date',
            'talent',
        )
