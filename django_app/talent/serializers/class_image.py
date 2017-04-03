from rest_framework import serializers

from talent.models import ClassImage

__all__ = (
    'ClassImageSerializer',
)


class ClassImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassImage
        fields = (
            'talent',
            'image'
        )
