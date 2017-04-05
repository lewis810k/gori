from django.contrib.auth import get_user_model
from rest_framework import serializers

from member.models import Tutor

__all__ = (
    'UserSerializer',
    'TutorSerializer',
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
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
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TutorSerializer(DynamicFieldsModelSerializer):
    user_id = serializers.CharField(
        read_only=True, source='user.username')
    name = serializers.CharField(
        read_only=True, source='user.name'
    )
    cellphone = serializers.CharField(
        read_only=True, source='user.cellphone'
    )
    profile_image = serializers.ImageField(
        read_only=True, source='user.profile_image')
    nickname = serializers.CharField(read_only=True, source='user.nickname')

    class Meta:
        model = Tutor
        fields = (
            'pk',
            'user_id',
            'name',
            'nickname',
            'is_verified',
            'profile_image',
            'cellphone',
        )
