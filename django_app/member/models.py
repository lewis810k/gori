from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from storages.backends.overwrite import OverwriteStorage


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        print('test')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class GoriUser(AbstractUser):
    USER_TYPE = (
        ('d', 'Django'),
        ('f', 'Facebook'),
    )
    name = models.CharField(max_length=30, blank=False, error_messages={'invalid': 'your custom error message'})
    nickname = models.CharField(max_length=15, blank=True, )
    cellphone = models.CharField(max_length=11, blank=True)
    profile_image = models.ImageField(upload_to='member/profile_image',
                                      blank=True,
                                      )
    user_type = models.CharField(choices=USER_TYPE, max_length=1, default='d')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_tutor = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True, unique=False)

    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

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
