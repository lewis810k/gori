from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from talent.models import Talent


class Review(models.Model):
    talent = models.ForeignKey(Talent, related_name='reviews', default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
    curriculum = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                     help_text='5이하의 숫자를 입력하세요')
    readiness = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                    help_text='5이하의 숫자를 입력하세요')
    timeliness = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                     help_text='5이하의 숫자를 입력하세요')
    delivery = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                   help_text='5이하의 숫자를 입력하세요')
    friendliness = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                       help_text='5이하의 숫자를 입력하세요')
    comment = models.TextField(blank=True)

    @property
    def average_rate(self):
        return (self.curriculum + self.readiness + self.timeliness + self.delivery + self.friendliness) / 5

    def comment_summary(self):
        return '{}...'.format(self.comment[0:10])
