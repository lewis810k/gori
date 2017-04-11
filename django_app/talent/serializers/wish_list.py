from django.contrib.auth import get_user_model
from rest_framework import serializers

from talent.models import WishList, Talent
from talent.serializers import TalentShortInfoSerializer

__all__ = (
    'WishListSerializer',
    'MyWishListSerializer',

)

User = get_user_model()


class WishListSerializer(serializers.ModelSerializer):
    talent = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), write_only=True)
    talent_title = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.title')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
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
                message=("이미 추가한 수업 입니다.")
            )
        ]


class MyWishListSerializer(serializers.ModelSerializer):
    talent = TalentShortInfoSerializer(many=True, source='talent_set')
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
            'talent',
        )
