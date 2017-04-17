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
    """
    curriculum을 생성하는 API 테스트
    data_list =
    """
    def test_create_curriculum(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])

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
            print(data)
            url = reverse('api:talent:curriculum-create')
            response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + data_item[2])
            print('31231243254325432523452345', response.data)


class CurriculumRetrieveTest(APITestUserLogin, APITestListVerify):
    """
    커리큘럼이 url이 존재하고 그 정보를 잘 받아오는지 확인하는 테스트 코드
    """
    def test_curriculum_retrieve_url_exist(self):
        #유저, 유저토큰, 튜터, 커리큘럼, 생성
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        curriculum = self.create_curriculum(talent, user_token)

        #url에 get 요청을 하여 데이터를 받아오고 필드 값이 정확하게 있는지 검사
        url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        field_list = ['talent_pk', 'information', 'image']
        self.verify_util(list(response.data['results'][0]), field_list)

        #잘못된 talent pk 를 넣었을때 오류코드가 잘 작동하는지 검사
        # url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': 123})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
