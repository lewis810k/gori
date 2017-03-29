from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import NoReverseMatch
from django.urls import resolve
from rest_framework.test import APILiveServerTestCase

from member.models import Tutor

User = get_user_model()


class MemberTest(APILiveServerTestCase):
    test_email = 'test@email.com'
    test_password = 'password'

    @staticmethod
    def create_user():
        user = User.objects.create(
            email='test@email.com',
            password='password',
        )
        return user

    def test_create_user(self):
        user = self.create_user()
        self.assertEqual(user.email, self.test_email)
        self.assertEqual(User.objects.count(), 1)

    def test_apis_url_exist(self):
        """
        현재 로그인 된 유저의 프로필과 특정 튜터의 프로필 정보를 받는 URL에 대한 검증
        """
        try:
            resolve('/api/member/profile/user/')
            resolve('/api/member/profile/tutor/1/')
        except NoReverseMatch as e:
            self.fail(e)

    def test_create_tutor(self):
        """
        tutor 생성 후 확인
        """
        user = self.create_user()
        tutor = Tutor.objects.create(
            user=user,
        )

        self.assertEqual(tutor.verification_method, 'UN')
        self.assertEqual(tutor.user, user)
