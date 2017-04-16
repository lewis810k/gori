from django.conf import settings
from django.db import models

from .talent import Talent

__all__ = (
    'Location',
)


class Location(models.Model):
    SCHOOL = (
        ('KOU', '고려대'),
        ('SNU', '서울대'),
        ('YOU', '연세대'),
        ('HOU', '홍익대'),
        ('EWWU', '이화여대'),
        ('BSU', '부산대'),
        ('JAU', '중앙대'),
        ('GGU', '건국대'),
        ('HYU', '한양대'),
        # ('GWU', '광운대'),
        # ('SMWU', '숙명여대'),
        # ('SSWU', '성신여대'),
        # ('KMU', '국민대'),
        # ('SWU', '서울여대'),
        # ('SGU', '서강대'),
        # ('MJU', '명지대'),
        # ('KIU', '한국외대'),
        # ('SSU', '숭실대'),
        # ('HYJ', '한예종'),
        # ('DGU', '동국대'),
        # ('STU', '서울과기대'),
        # ('DSWU', '덕성여대'),
        # ('SEU', '서울교대'),
        # ('DDWU', '동덕여대'),
    )
    AREA = (
        ('KN', '강남'),
        ('SC', '신촌'),
        ('SD', '사당'),
        ('JS', '잠실'),
        ('JR', '종로'),
        ('HH', '혜화'),
        ('YS', '용산'),
        ('HJ', '합정'),
        ('MD', '목동'),
        ('ETC', '기타'),
    )
    SPECIFIC_LOCATION = (
        ('NEGO', '협의 후 결정'),
        ('SELF', '직접 입력'),
    )
    DAYS_OF_WEEK = (
        ('MO', '월'),
        ('TU', '화'),
        ('WE', '수'),
        ('TH', '목'),
        ('FR', '금'),
        ('SA', '토'),
        ('SU', '일'),
    )
    EXTRA_FEE = (
        ('Y', '예, 있습니다'),
        ('N', '아니오, 없습니다'),
    )
    REGION = AREA + SCHOOL
    talent = models.ForeignKey(Talent, limit_choices_to={'is_soldout': False}, related_name='locations')
    registered_student = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Registration',
    )
    region = models.CharField(choices=REGION, max_length=4)
    specific_location = models.CharField(choices=SPECIFIC_LOCATION, max_length=4, help_text='상세 위치 정보')
    location_info = models.TextField(blank=True)
    extra_fee = models.CharField(choices=EXTRA_FEE, max_length=1, default='N', help_text='장소 및 기타 비용이 있나요?')
    extra_fee_amount = models.CharField(max_length=50, help_text='추가 비용: 예시) 재료 비용 1만원', blank=True)
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=2)
    time = models.CharField(max_length=50, help_text=',로 나누어 입력해 주세요. 예시) 13-14시, 18-19시')

    def __str__(self):
        return '{} - 지역: {}'.format(self.talent, self.get_region_display())

    @property
    def time_list(self):
        time_list = self.time.split(',')
        return time_list
