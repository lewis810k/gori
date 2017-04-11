from rest_framework import serializers

from member.models import GoriUser, Tutor
from talent.models import Talent, Question, Reply

__all__ = (
    # 'QnaSerializer',
    'ReplySerializer',
    'QnAWrapperSerializer',
    'QuestionSerializer',
)


class ReplySerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all(), source='tutor.user.name')
    tutor_image = serializers.ImageField(source='tutor.user.profile_image')
    content = serializers.CharField(source='answer')

    class Meta:
        model = Reply
        fields = (
            'tutor',
            'tutor_image',
            'content',
            'created_date',
        )


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='user.name')
    user_image = serializers.ImageField(source='user.profile_image')
    answer = ReplySerializer()

    class Meta:
        model = Question
        fields = (
            'user',
            'user_image',
            'question',
            'created_date',
            'answer',
        )

        # def get_user_image(self, obj):
        #     print(obj.user)
        #     # print(dir(obj.user.profile_image))
        #     return obj.user


class QnAWrapperSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'QnA'
        )

    def create(self, validated_data):
        qna = validated_data.pop('title')
        # photos = validated_data.pop('photo_set')
        print(qna)

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()
