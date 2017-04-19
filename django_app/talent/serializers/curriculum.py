from rest_framework import serializers

from talent.models import Curriculum, Talent

__all__ = (
    'CurriculumSerializer',
    'CurriculumUpdateSerializer',
    'CurriculumCreateSerializer'
)


class CurriculumSerializer(serializers.ModelSerializer):
    talent_pk = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.id')

    class Meta:
        model = Curriculum
        fields = (
            'talent_pk',
            'information',
            'image',
        )


class CurriculumCreateSerializer(serializers.ModelSerializer):
    talent_pk = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent')

    class Meta:
        model = Curriculum
        fields = (
            'talent_pk',
            'information',
            'image',
        )


class CurriculumUpdateSerializer(serializers.ModelSerializer):
    curriculum_pk = serializers.IntegerField(source='pk')

    class Meta:
        model = Curriculum
        fields = (
            'information',
            'image'
        )
