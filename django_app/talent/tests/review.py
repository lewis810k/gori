from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Review
from utils import APITest_User_Login

__all__ = (
    'ReviewCreateTest',
    'ReviewRetrieveTest'
)

class ReviewCreateTest(APILiveServerTestCase, APITest_User_Login):
    def test_create_review(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        fail_list = [
            [1234, 'readiness', user_token[1]],
            [talent.pk, '', user_token[1]],
            [talent.pk, 'readiness', user_token[0]],
            [talent.pk, 'readiness', user_token[1]],
            [talent.pk, 'readiness', ""],
        ]
        for fail_item in fail_list:
            data = {
                'talent_pk': fail_item[0],
                'curriculum': 5,
                fail_item[1]: 5,
                'timeliness': 5,
                'delivery': 5,
                'friendliness': 5,
                'comment': 'test_comment'
            }
            url = reverse('api:talent:review-create')
            response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + fail_item[2])
            if fail_item[1] == "":
                self.assertIn('non_field_error', response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            elif fail_item[0] == talent.pk and fail_item[1] == 'readiness' and fail_item[2] == user_token[1]:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(Review.objects.count(), 1)
            elif fail_item[2] == "":
                self.assertIn('detail', response.data)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            else:
                self.assertIn('detail', response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[1])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)


class ReviewRetrieveTest(APILiveServerTestCase, APITest_User_Login):
    def test_review_retrieve_url_exist(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        review = self.create_review(talent, user_token[1])

        url = reverse('api:talent:review-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        response_list = list(response.data) + list(response.data['reviews'][0]) \
                        + list(response.data['reviews'][0]['user'])
        field_list = ['pk', 'title', 'category', 'type', 'average_rates', 'review_count', 'reviews', 'talent', 'user',
                      'curriculum', 'readiness', 'timeliness', 'delivery', 'friendliness', 'created_date', 'comment',
                      'name', 'profile_image']

        for field_item in field_list:
            self.assertIn(field_item, response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:talent:review-retrieve', kwargs={'pk': 555})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
