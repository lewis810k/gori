from django.conf import settings
from django.db import models

from talent.models import Location

__all__ = (
    'Registration',
)


class Registration(models.Model):
    LEVEL = (
        (1, '입문자'),
        (2, '초/중급자'),
        (3, '상급자'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='registrations')
    talent_location = models.ForeignKey(Location,
                                        related_name='registrations')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    student_level = models.IntegerField(choices=LEVEL,
                                        help_text="레벨 선택", default=1)
    experience_length = models.IntegerField(default=0, blank=True,
                                            help_text="해당 수업관련 경력을 개월로 입력")
    message_to_tutor = models.CharField(max_length=50,
                                        help_text="수강신청시 유저가 튜터에게 보내는 메세지", blank=False)

    def __str__(self):
        return '{} 님  {}: {} 수업을 신청하였습니다'.format(self.student.username, self.talent_location.talent.pk,
                                                 self.talent_location.talent.title)
