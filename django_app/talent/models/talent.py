from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from config import settings
from member.models import Tutor

__all__ = (
    'Talent',
)


class Talent(models.Model):
    CATEGORY = (
        ('HNB', '헬스 / 뷰티'),
        ('LAN', '외국어'),
        ('COM', '컴퓨터'),
        ('ART', '미술 / 음악'),
        ('SPO', '스포츠'),
        ('JOB', '전공 / 취업'),
        ('HOB', '이색취미'),
        ('ETC', '기타'),
    )
    TYPE_CHOICE = (
        (0, '1:1 수업'),
        (1, '그룹 수업'),
        (2, '원데이 수업'),
    )

    tutor = models.ForeignKey(Tutor)
    wishlist_user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='WishList')
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30, blank=False)
    category = models.CharField(choices=CATEGORY, max_length=3, blank=False, default='HNB')
    type = models.IntegerField(choices=TYPE_CHOICE, default=1, blank=False)
    cover_image = models.ImageField(upload_to='talent/cover_image')
    tutor_info = models.CharField(max_length=80, blank=False)
    class_info = models.CharField(max_length=150, blank=False)
    video1 = models.URLField(blank=True)
    video2 = models.URLField(blank=True)
    price_per_hour = models.IntegerField(blank=False, help_text='시간당 가격')
    hours_per_class = models.IntegerField(blank=False, help_text='기본 수업 시간')
    number_of_class = models.IntegerField(blank=False, help_text='한달 기준 총 수업 일')
    is_soldout = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    min_number_student = models.IntegerField(default=1, validators=[MaxValueValidator(9), MinValueValidator(1)])
    max_number_student = models.IntegerField(default=1, validators=[MaxValueValidator(9), MinValueValidator(1)])
    tutor_message = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_category(self, obj):
        return obj.get_category_dispaly()

    @property
    def registration_count(self):
        count = 0
        for l in self.locations.all():
            count += l.registrations.count()
        return count

    @property
    def region_list(self):
        region_list = []
        for location in self.locations.all():
            region_list.append(location.get_region_display())
        return region_list
