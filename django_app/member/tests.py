# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# # Create your tests here.
# from django.urls import NoReverseMatch
# from django.urls import resolve
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APILiveServerTestCase
#
# from member.models import Tutor
#
# User = get_user_model()
#
#
# class MemberTest(APILiveServerTestCase):
#     test_user = 'test'
#     test_password1 = 'qwer1234'
#     test_password2 = 'qwer1234'
#
#     def create_user(self):
#         data = {
#             'username': self.test_user,
#             'password1': self.test_password1,
#             'password2': self.test_password2,
#         }
#         url = reverse('rest_register')
#         response = self.client.post(url, data=data)
#         print(response.data)
#         return response
#
#     def test_create_and_register_user(self):
#         """
#         'rest_register'를 name으로 가지는 url을 불러온다.
#         rest_auth/registration/urls.py에 있음
#         해당 url로 post 요청을 보내서 응답을 확인한다.
#         """
#         response = self.create_user()
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         user = User.objects.last()
#         self.assertEqual(user.username, self.test_user)
#
#     # def test_delete_user(self):
#     #     """
#     #     유저 삭제 테스트
#     #     """
#         # self.create_user()
#         # url = reverse('api:user-delete', kwargs={'pk': '1'})
#         # print(url)
#
#
#
#         # def test_apis_url_exist(self):
#         #     """
#         #     현재 로그인 된 유저의 프로필과 특정 튜터의 프로필 정보를 받는 URL에 대한 검증
#         #     """
#         #     try:
#         #         resolve('/api/member/profile/user/')
#         #         resolve('/api/member/profile/tutor/1/')
#         #     except NoReverseMatch as e:
#         #         self.fail(e)
#
#         # def test_create_tutor(self):
#         #     """
#         #     tutor 생성 후 확인
#         #     """
#         #     user = self.create_user()
#         #     tutor = Tutor.objects.create(
#         #         user=user,
#         #     )
#         #
#         #     self.assertEqual(tutor.verification_method, 'UN')
#         #     self.assertEqual(tutor.user, user)
