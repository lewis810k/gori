from django.contrib.auth import get_user_model
from rest_framework import serializers

from member.models import Tutor
from talent.models import Talent, Question, Reply

__all__ = (
    # 'QnaSerializer',
    'ReplySerializer',
    'ReplyCreateSerializer',
    'ReplyUpdateSerializer',
    'QuestionSerializer',
    'QuestionCreateSerializer',
    'QuestionUpdateSerializer'
)

User = get_user_model()


class ReplySerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all(), source='tutor.user.name')
    tutor_image = serializers.ImageField(source='tutor.user.profile_image')

    class Meta:
        model = Reply
        fields = (
            'pk',
            'tutor',
            'tutor_image',
            'created_date',
            'content',
        )


class ReplyCreateSerializer(serializers.ModelSerializer):
    question_pk = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all())

    class Meta:
        model = Reply
        fields = (
            'question_pk',
            'tutor',
            'content',
        )


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            'content'
        )


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user.name')
    user_image = serializers.ImageField(source='user.profile_image')
    replies = ReplySerializer(source='reply_set', many=True)

    class Meta:
        model = Question
        fields = (
            'pk',
            'user',
            'user_image',
            'created_date',
            'content',
            'replies',
        )


class QuestionCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    talent_pk = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), source='talent')

    class Meta:
        model = Question
        fields = (
            'user',
            'talent_pk',
            'content',
        )


class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'content'
        )
