from django.conf import settings
from django.db import models

from member.models import Tutor
from talent.models import Talent


__all__ = (
    'Question',
)

class Question(models.Model):
    talent = models.ForeignKey(Talent)

