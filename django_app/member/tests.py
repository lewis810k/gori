from django.contrib.auth import get_user_model

# Create your tests here.

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITest_User_Login

User = get_user_model()


class MemberTest(APILiveServerTestCase,APITest_User_Login):
    test_user = 'test'
    test_password1 = 'qwer1234'
    test_password2 = 'qwer1234'
    test_name = 'testname'

    def create_user(self, num=1):
        users = []
        for i in range(num):
            user = User.objects.create_user(
                username='test_username{}'.format(i + 1),
                name='test{}'.format(i + 1),
                password='votmxmzoa',
            )
            users.append(user)
        if num == 1:
            return user

    def test_signup(self):
        data = {
            'username': self.test_user,
            'password1': self.test_password1,
            'password2': self.test_password2,
            'name': self.test_name,
        }
        url = reverse('api:member:user-signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_obtain_token(self):
        user = self.create_user()
        self.assertEqual(User.objects.count(), 1)
        data = {
            'username': user.username,
            'password': 'votmxmzoa',
        }
        url = reverse('api:member:user-token')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_login(self):
        user = self.create_user()
        self.assertEqual(User.objects.count(), 1)
        data = {
            'username': user.username,
            'password': 'votmxmzoa',
        }
        url = reverse('api:member:rest_login')
        response = self.client.post(url, data, format='json')
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        token = self.test_obtain_token()
        print(token.data.get('token'))
        self.assertEqual(User.objects.count(), 1)
        url = reverse('api:member:rest_logout')
        response = self.client.post(url, HTTP_AUTHORIZATION='Token ' + token.data.get('token'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_url_exist(self):
        token = self.test_obtain_token()
        url = reverse('api:member:user-detail')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token.data.get('token'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)




# def test_create_and_register_user(self):
#     """
#     'rest_register'를 name으로 가지는 url을 불러온다.
#     rest_auth/registration/urls.py에 있음
#     해당 url로 post 요청을 보내서 응답을 확인한다.
#     """
#     response = self.create_user()
#     self.assertEqual(User.objects.count(), 1)
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     user = User.objects.last()
#     self.assertEqual(user.username, self.test_user)

# def test_delete_user(self):
#     """
#     유저 삭제 테스트
#     """
# self.create_user()
# url = reverse('api:user-delete', kwargs={'pk': '1'})
# print(url)



# def test_apis_url_exist(self):
#     """
#     현재 로그인 된 유저의 프로필과 특정 튜터의 프로필 정보를 받는 URL에 대한 검증
#     """
#     try:
#         resolve('/api/member/profile/user/')
#         resolve('/api/member/profile/tutor/1/')
#     except NoReverseMatch as e:
#         self.fail(e)

# def test_create_tutor(self):
#     """
#     tutor 생성 후 확인
#     """
#     user = self.create_user()
#     tutor = Tutor.objects.create(
#         user=user,
#     )
#
#     self.assertEqual(tutor.verification_method, 'UN')
#     self.assertEqual(tutor.user, user)
