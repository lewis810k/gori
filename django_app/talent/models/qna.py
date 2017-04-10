from django.conf import settings
from django.db import models

from member.models import Tutor
from talent.models import Talent

__all__ = (
    'Question',
    'Answer',
)


class Question(models.Model):
    talent = models.ForeignKey(Talent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.OneToOneField(Question)
    tutor = models.ForeignKey(Tutor)
    answer = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)


