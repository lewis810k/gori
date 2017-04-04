from rest_framework import serializers

from talent.models import ClassImage, Talent

__all__ = (
    'ClassImageSerializer',
    'ClassImageWrapperSerializers',
)


class ClassImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassImage
        fields = (
            'image',
        )


class ClassImageWrapperSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class_image = ClassImageSerializer(many=True, source='classimage_set')

    class Meta:
        model = Talent
        fields = (
            'id',
            'title',
            'category',
            'type',
            'class_image',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()
