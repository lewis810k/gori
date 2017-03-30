from django.contrib.auth import get_user_model
from rest_framework import serializers

from member.models import Tutor

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'name',
            'user_type',
            'is_staff',
            'is_active',
            'cellphone',
            'profile_image',
            'joined_date',
            'is_tutor',
            'last_login',
        )

    def get_user_type(self, obj):
        return obj.get_user_type_display()

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            'pk',
            'user',
            'is_verified',
        )
