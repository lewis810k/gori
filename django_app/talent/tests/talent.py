from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Talent
from utils import APITest_User_Login, image_upload, Tutor

User = get_user_model()

__all__ = (
    'TutorTest',
    'TalentCreateTest',
    'TalentListTest',
)

class TutorTest(APILiveServerTestCase, APITest_User_Login):
    def test_tutor_register(self):
        """
        유저를 tutor로 등록시키는 코드
        :return:
        """
        user, token = self.obtain_token(2)
        token = token[0]
        user_token = token[1]
        test_image = image_upload()
        data = {
            'verification_method': 'UN',
            'verification_images': test_image,
            'school': 'test_university',
            'major': 'test_major',
            'current_status': 'E'
        }
        fail_data = {
            'verification_method': 'ZX',
            'verification_images': test_image,
            'school': 'test_university',
            'major': 'test_major',
            'current_status': 'E'
        }
        url = reverse('api:member:tutor-register')
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + token)
        self.assertIn('detail', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutor.objects.count(), 1)
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TalentCreateTest(APILiveServerTestCase, APITest_User_Login):
    def test_create_talent(self):
        test_image = image_upload()
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        data = {
            'title': 'test',
            'category': 'COM',
            'type': 1,
            'tutor_info': 'test_info',
            'class_info': 'test_class_info',
            'number_of_class': 5,
            'price_per_hour': 20000,
            'hours_per_class': 2,
            'cover_image': test_image,
            'video1': 'test.com',
            'video2': 'test2.com'
        }
        fail_data = {
            'title': 'test1',
            'category': 'COM',
            'type': 1,
            'tutor_info': 'test_info',
            'class_info': 'test_class_info',
            'number_of_class': 5,
            'hours_per_class': 2,
            'cover_image': test_image,
            'video1': 'test.com',
            'video2': 'test2.com'
        }
        title_overlap_fail_data = {
            'title': 'test',
            'category': 'COM',
            'type': 1,
            'tutor_info': 'test_info',
            'class_info': 'test_class_info',
            'number_of_class': 5,
            'price_per_hour': 20000,
            'hours_per_class': 2,
            'cover_image': test_image,
            'video1': 'test.com',
            'video2': 'test2.com'
        }
        url = reverse('api:talent:create')
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertIn('detail', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Talent.objects.count(), 1)
        response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, title_overlap_fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token[1])


class TalentListTest(APILiveServerTestCase, APITest_User_Login):
    def test_talent_list(self):
        """
        params : resgion:SD 은 사당으로 검색하기에
        :return:
        """
        #
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        location = self.create_location(talent, user_token)
        url = reverse('api:talent:list')
        response = self.client.get(url)
        results = response.data['results'][0]

        field_list = ['pk', 'title', 'category', 'type', 'tutor', 'tutor', 'user_id', 'name', 'nickname', 'is_verified',
                      'profile_image', 'cellphone', 'is_school', 'cover_image', 'price_per_hour', 'hours_per_class',
                      'number_of_class', 'min_number_student', 'max_number_student', 'is_soldout', 'created_date',
                      'average_rate', 'review_count', 'registration_count', 'regions']
        response_list = list(results.keys()) + list(results["tutor"])

        for field in field_list:
            self.assertIn(field, response_list)

        params_list = [
            ({'region': 'KN'}, 1),
            ({'region': 'SD'}, 0),
            ({'title': 'test'}, 1),
            ({'title': 'qwer'}, 0),
            ({'category': 'COM'}, 1),
            ({'category': 'SPO'}, 0),
        ]
        url = reverse('api:talent:list')
        for param_item in params_list:
            response = self.client.get(url, param_item[0])
            self.assertEqual(response.data['count'], param_item[1])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talent_detail_retrieve_all_url_exist(self):
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        url = reverse('api:talent:detail-all', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        field_list = ['pk', 'title', 'category', 'type', 'tutor', 'tutor', 'user_id', 'name', 'nickname', 'is_verified',
                      'profile_image', 'cellphone', 'cover_image', 'price_per_hour', 'hours_per_class',
                      'number_of_class', 'min_number_student', 'max_number_student',
                      'average_rate', 'review_count']
        # 'registration_count', 모델다시 해놓고 바꿔줄것
        response_list = list(response.data) + list(response.data["tutor"])

        for field in field_list:
            self.assertIn(field, response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:talent:detail-all', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_talent_detail_short_retrieve_url_exist(self):
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        url = reverse('api:talent:detail-short', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        field_list = ['max_number_student', 'price_per_hour', 'is_verified', 'category', 'number_of_class',
                      'hours_per_class', 'is_soldout', 'class_info', 'video1', 'video2', 'pk', 'title', 'tutor',
                      'user_id', 'name', 'nickname', 'profile_image', 'cellphone', 'type', 'cover_image',
                      'tutor_info', 'average_rate', 'review_count', 'min_number_student']
        response_list = list(response.data) + list(response.data["tutor"])

        for field in field_list:
            self.assertIn(field, response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:talent:detail-all', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
