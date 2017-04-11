from rest_framework import serializers

from talent.models import Curriculum, Talent

__all__ = (
    'CurriculumSerializer',
    'CurriculumWrapperSerializer',
)


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            'talent',
            'information',
            'image',
        )


class CurriculumWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    curriculums = CurriculumSerializer(many=True, source='curriculum_set')

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'curriculums',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()
