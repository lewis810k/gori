from django.db import models

from talent.models import Talent

__all__ = (
    'Curriculum',
)


class Curriculum(models.Model):
    talent = models.ForeignKey(Talent, )
    information = models.CharField(max_length=50)
    image = models.ImageField(upload_to='talent/curriculum', blank=True)

    class Meta:
        ordering = ['pk', ]

    def __str__(self):
        return 'Talent {}: {}'.format(self.talent.id, self.id)
