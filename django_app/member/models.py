from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class GoriUser(AbstractUser):
    USER_TYPE = (
        ('d', 'Django'),
        ('f', 'Facebook'),
    )
    name = models.CharField(max_length=30, blank=False, error_messages={'invalid': 'your custom error message'})
    nickname = models.CharField(max_length=15, blank=True, )
    cellphone = models.CharField(max_length=11, blank=True)
    profile_image = models.ImageField(upload_to='member/profile_image',
                                      blank=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=1, default='d')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_tutor = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.username, self.name)

    def create_tutor(self, nickname, cellphone, profile_image,
                     verification_method, verification_images,
                     **extra_fields):
        user = GoriUser.objects.get(username=self.username)
        user.is_tutor = True
        user.nickname = nickname
        user.cellphone = cellphone
        user.profile_image = profile_image
        user.save()
        tutor = Tutor.objects.create(user=user, verification_method=verification_method,
                                     verification_images=verification_images, **extra_fields)

        return tutor

    def clean_name(self):
        raise ValidationError({'bark_volume': ["Must be louder!", ]})


class Tutor(models.Model):
    VERIFICATION_CHOICES = (
        ('UN', '대학생'),
        ('GR', '대학원생'),
        ('ID', '신분증'),
    )
    STUDENT_STATUS = (
        ('G', '졸업'),
        ('E', '재학'),
        ('I', '수료'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_method = models.CharField(choices=VERIFICATION_CHOICES, max_length=2, default='ID')
    verification_images = models.ImageField(upload_to='member/verification_image')
    school = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)
    current_status = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.user.username
