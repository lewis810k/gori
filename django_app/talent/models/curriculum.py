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
        return 'Tutor : {}, Talent : {}'.format(self.talent.tutor.user.name, self.talent.title)
