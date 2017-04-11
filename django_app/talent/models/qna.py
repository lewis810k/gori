from django.conf import settings
from django.db import models

from member.models import Tutor
from talent.models import Talent

__all__ = (
    'Question',
    'Reply',
)


class Question(models.Model):
    talent = models.ForeignKey(Talent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    question = models.ForeignKey(Question)
    tutor = models.ForeignKey(Tutor)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


