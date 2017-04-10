from django.conf import settings
from django.db import models

from member.models import Tutor
from talent.models import Talent


__all__ = (
    'Question',
)

class Question(models.Model):
    talent = models.ForeignKey(Talent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    quesetion = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    pass
