from rest_framework import serializers

from member.models import GoriUser
from talent.models import Talent, WishList

__all__ = (
    'WishListSerializer',
)


class WishListSerializer(serializers.ModelSerializer):
    talent = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), write_only=True)
    talent_title = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.class_title')
    user = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), write_only=True)
    user_name = serializers.PrimaryKeyRelatedField(read_only=True, source='user.name')

    class Meta:
        model = WishList
        fields = (
            'talent',
            'talent_title',
            'user_name',
            'user',
            'added_date'
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=WishList.objects.all(),
                fields=('talent', 'user'),
                message=("Some custom message.")
            )
        ]
