from rest_framework import serializers

from talent.models import Talent

__all__ = (
    # 'QnaSerializer',
    'QnaWrapperSerializer',
)


# class QnaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Qna
#         fields = (
#             'talent',
#             'user',
#             'question',
#             'answer',
#             'Qna',
#             'tutor'
#         )


class QnaWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    # Qna = QnaSerializer(many=True, source='qna_set')

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            # 'Qna',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()
