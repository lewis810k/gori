from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITest_User_Login

User = get_user_model()


class UserSignUpLoginTest(APILiveServerTestCase, APITest_User_Login):
    test_user = 'test'
    test_password1 = 'testpw12'
    test_password2 = 'testpw12'
    test_name = 'testname'

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
            'password': 'testpw12',
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
            'password': 'testpw12',
        }
        url = reverse('api:member:rest_login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        token = self.test_obtain_token()
        self.assertEqual(User.objects.count(), 1)
        url = reverse('api:member:rest_logout')
        response = self.client.post(url, HTTP_AUTHORIZATION='Token ' + token.data.get('token'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MemberProfileTest(APILiveServerTestCase, APITest_User_Login):
    def test_user_detail_retrieve(self):
        user, token = self.obtain_token()
        url = reverse('api:member:user-detail')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user_id'), user.username)
        invalid_token = "asdf"
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token + invalid_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_update(self):
        user, token = self.obtain_token()
        patch_user_url = reverse('api:member:user-patch')
        new_nickname = "영나"
        new_name = "new_test_name"
        new_cellphone = "01099937576"
        data = {
            'nickname': new_nickname,
            "cellphone": new_cellphone,
            "name": new_name,
        }
        response = self.client.patch(patch_user_url, data=data, HTTP_AUTHORIZATION='Token ' + token)
        user = User.objects.get(username=user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.cellphone, new_cellphone)
        self.assertEqual(user.nickname, new_nickname)
        self.assertEqual(user.name, new_name)
        invalid_cellphone = "99djhjhgsdf32"
        invalid_data_1 = {
            "cellphone": invalid_cellphone,
        }
        response = self.client.patch(patch_user_url, invalid_data_1, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        invalid_data_2 = {
            "nickname123": new_nickname
        }
        response = self.client.patch(patch_user_url, invalid_data_2, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
