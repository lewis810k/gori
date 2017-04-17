from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Review
from utils import APITestUserLogin, APITestListVerify

__all__ = (
    'ReviewCreateTest',
    'ReviewRetrieveTest'
)


class ReviewCreateTest(APILiveServerTestCase, APITestUserLogin):
    def test_create_review(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        data_list = [
            ["", user_token[1]],
            [1234, user_token[1]],
            [talent.pk, user_token[1]],
            [talent.pk, user_token[0]],
            [talent.pk, ""],
        ]
        for data_item in data_list:
            data = {
                'talent_pk': data_item[0],
                'curriculum': 5,
                'readiness': 5,
                'timeliness': 5,
                'delivery': 5,
                'friendliness': 5,
                'comment': 'test_comment'
            }
            url = reverse('api:talent:review-create')
            response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + data_item[1])
            if data_item[0] == talent.pk and data_item[1] == user_token[1]:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(Review.objects.count(), 1)
            elif data_item[0] == '' or data_item[0] == 1234:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('talent_pk', response.data)
            elif data_item[1] == user_token[0]:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('detail', response.data)
            else:
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertIn('detail', response.data)

                # 지금은 리뷰가 여러개 달림
                # response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[1])
                # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                # self.assertEqual(Review.objects.count(), 1)


class ReviewRetrieveTest(APITestUserLogin, APITestListVerify):
    def test_review_list_url_exist(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        review = self.create_review(talent, user_token[1])

        url = reverse('api:talent:review-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        field_list = ['pk', 'user', 'curriculum', 'readiness', 'timeliness', 'delivery', 'friendliness', 'created_date',
                      'comment', 'name', 'profile_image']

        data = list(response.data['results'][0]) + list(response.data['results'][0]['user'])
        self.verify_util(data, field_list)

        # url = reverse('api:talent:review-retrieve', kwargs={'pk': 555})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
