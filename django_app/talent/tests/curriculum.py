from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITest_User_Login, image_upload

User = get_user_model()

__all__ = (
    'CurriculumCreateTest',
    'CurriculumRetrieveTest'
)


class CurriculumCreateTest(APILiveServerTestCase, APITest_User_Login):
    def test_create_curriculum(self):
        print('43427534285934278953427895342789')
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        test_image = image_upload()
        data = {
            'talent_pk': talent.pk,
            'information': 'test_information',
            'image': test_image,
        }
        url = reverse('api:talent:curriculum-create')
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        fail_list = [
            ['talent_pk', 555],
            ["", ""]
        ]
        for fail_item in fail_list:
            fail_data = {
                fail_item[0]: fail_item[1],
                'information': 'test_information',
                'image': test_image,
            }
            url = reverse('api:talent:curriculum-create')
            response = self.client.post(url, fail_data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            if fail_item[0] == "":
                self.assertIn('non_field_error', response.data)
            else:
                self.assertIn('detail', response.data)
        fail_token = [
            user_token[1],
            ""
        ]
        for fail_item in fail_token:
            url = reverse('api:talent:curriculum-create')
            response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + fail_item)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CurriculumRetrieveTest(APILiveServerTestCase, APITest_User_Login):
    def test_curriculum_retrieve_url_exist(self):
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        curriculum = self.create_curriculum(talent, user_token)

        url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_list = list(response.data) + list(response.data['curriculums'][0])
        field_list = ['pk', 'title', 'category', 'type', 'curriculums', 'talent_pk', 'information', 'image']
        for field_item in field_list:
            self.assertIn(field_item, response_list)
        url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
