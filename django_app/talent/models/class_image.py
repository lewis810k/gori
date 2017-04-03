from django.db import models

from talent.models import Talent

__all__ = (
    'ClassImage',
)


class ClassImage(models.Model):
    talent = models.ForeignKey(Talent)
    image = models.ImageField(upload_to='talent/extra_images')
