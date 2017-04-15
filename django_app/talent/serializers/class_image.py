from rest_framework import serializers

from talent.models import ClassImage, Talent

__all__ = (
    'ClassImageSerializer',
    'ClassImageCreateSerializer',
)


class ClassImageSerializer(serializers.ModelSerializer):
    talent_pk = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.id')

    class Meta:
        model = ClassImage
        fields = (
            'pk',
            'talent_pk',
            'image',
        )


class ClassImageCreateSerializer(serializers.ModelSerializer):
    talent_pk = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent')

    class Meta:
        model = ClassImage
        fields = (
            'talent_pk',
            'image',
        )
