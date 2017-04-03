from django.conf import settings
from django.db import models

from talent.models import Talent

__all__ = (
    'WishList',
)


class WishList(models.Model):
    talent = models.ForeignKey(Talent, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, )
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('talent', 'user',)
        )

    def __str__(self):
        return '{}'.format(self.user.name)

    def get_talent_title(self):
        return self.user.username
