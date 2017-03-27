from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = CustomUserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False,
                          is_active=False, is_superuser=False,
                          last_login=now, joined_date=now,
                          is_tutor=False, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        super_user = self.create_user(email, password, **extra_fields)
        super_user.is_staff = True
        super_user.is_active = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


class GoriUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=False)
    nickname = models.CharField(max_length=15, blank=True,)
    cellphone = models.CharField(max_length=11, blank=True)
    profile_image = models.ImageField(upload_to='member/profile_image',
                                      blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin '
                                             'site.')
    is_active = models.BooleanField(default=False,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_tutor = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'name',

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def create_tutor(self, nickname, cellphone, profile_image,
                     verification_method, verification_images,
                     **extra_fields):
        user = GoriUser.objects.get(email=self.email)
        user.is_tutor = True
        user.model(nickname=nickname, cellphone=cellphone, profile_image=profile_image)
        user.save()
        Tutor.objects.create(user=user, verification_method=verification_method,
                             verification_images=verification_images)
        return self.tutor


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
    verification_method = models.CharField(choices=VERIFICATION_CHOICES, max_length=2, default='UN')
    verification_images = models.ImageField(upload_to='member/verification_image')
    school = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)
    current_status = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.user.email
