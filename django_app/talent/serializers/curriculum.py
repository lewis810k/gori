from rest_framework import serializers

from talent.models import Curriculum

__all__ = (
    'CurriculumSerializer',
)


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            'talent',
            'information',
            'image',
        )
