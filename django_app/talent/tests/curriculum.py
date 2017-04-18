from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITestUserLogin, APITestListVerify
from utils.upload import image_upload

User = get_user_model()

__all__ = (
    'CurriculumCreateTest',
    'CurriculumRetrieveTest'
)


class CurriculumCreateTest(APILiveServerTestCase, APITestUserLogin):
    def test_create_curriculum(self):
        # 유저 유저토큰 튜터 탈렌트 생성
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])

        # 성공하는 데이터 모음과 실패하는 데이터 모음들을 묶음
        # 1.성공 나머지 실패
        data_list = [
            ['talent_pk', talent.pk, user_token[0]],
            ['talent_pk', 555, user_token[0]],
            ["", talent.pk, user_token[0]],
            ['talent_pk', talent.pk, user_token[1]],
            ['talent_pk', talent.pk, ""],
        ]
        for data_item in data_list:
            test_image = image_upload()
            data = {
                data_item[0]: data_item[1],
                'information': 'test_information',
                'image': test_image,
            }
            url = reverse('api:talent:curriculum-create')
            response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + data_item[2])
            if data_item[0] == 'talent_pk' and data_item[1] == talent.pk and data_item[2] == user_token[0]:
                self.assertIn('detail', response.data)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            elif data_item[0] == "" or data_item[1] == 555:
                self.assertIn('talent_pk', response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            elif data_item[2] == "":
                self.assertIn('detail', response.data)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            else:
                self.assertIn('detail', response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CurriculumRetrieveTest(APITestUserLogin, APITestListVerify):
    def test_curriculum_retrieve_url_exist(self):
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        curriculum = self.create_curriculum(talent, user_token)

        url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        field_list = ['talent_pk', 'information', 'image']
        self.verify_util(list(response.data['results'][0]), field_list)

        # url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': 123})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
