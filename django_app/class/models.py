from django.db import models

from member.models import Tutor, GoriUser


class GoriClass(models.Model):
    CATEGORY = (
        ('HNB', '헬스 / 뷰티'),
        ('LAN', '외국어'),
        ('COM', '컴퓨터'),
        ('ART', '미술 / 음악'),
        ('SPO', '스포츠'),
        ('JOB', '전공 / 취업'),
        ('HOB', '이색취미'),
    )
    CLASS_TYPE_CHOICE = (
        (0, '1:1'),
        (1, '그룹 수업'),
        (2, '원데이 수업'),
    )
    tutor = models.ForeignKey(Tutor, )
    class_title = models.CharField(max_length=30, blank=False)
    category = models.CharField(choices=CATEGORY, max_length=3, blank=False)
    class_type = models.IntegerField(choices=CLASS_TYPE_CHOICE, default='1', blank=False)
    cover_image = models.ImageField(upload_to='class/cover_image')
    tutor_info = models.CharField(max_length=80, blank=False)
    class_info = models.CharField(max_length=150, blank=False)
    video1 = models.URLField(blank=True)
    video2 = models.URLField(blank=True)
    price_per_hour = models.IntegerField(blank=False)
    hours_per_class = models.IntegerField(blank=False)
    number_of_class = models.IntegerField(blank=False)


class ClassImage(models.Model):
    gori_class = models.ForeignKey(GoriClass)
    class_image = models.ImageField(upload_to='class/extra_images')


class Registration(models.Model):
    student = models.ForeignKey(GoriUser)
    gori_class = models.ForeignKey(GoriClass)
    joined_date = models.DateTimeField(auto_now_add=True)
