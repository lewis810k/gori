from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from talent.models import Talent


class Review(models.Model):
    talent = models.ForeignKey(Talent, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
    curriculum_rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                          help_text='5이하의 숫자를 입력하세요')
    readiness_rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                         help_text='5이하의 숫자를 입력하세요')
    timeliness_rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                          help_text='5이하의 숫자를 입력하세요')
    delivery_rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                        help_text='5이하의 숫자를 입력하세요')
    friendliness_rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                                            help_text='5이하의 숫자를 입력하세요')
