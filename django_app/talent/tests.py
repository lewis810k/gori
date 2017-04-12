from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITest_User_Login


class GoriTest(APILiveServerTestCase, APITest_User_Login):
    def test_talent_list(self):
        """
        params : resgion:SD 은 사당으로 검색하기에
        :return:
        """
        #
        user = self.create_user()
        tutor = self.create_tutor(user)
        talent = self.create_talent(tutor)
        self.create_location(talent)
        params = {
            'region': 'SD'
        }
        url = reverse('api:talent:list')
        print(url)
        response = self.client.get(url, params)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 어떤 테스트인지
        params = {
            'title': 'test'
        }
        response = self.client.get(url, params)
        print(response.data)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # def test_url_exist(self):
        #     talent = self.create_talent()
        #     talent_list_url = reverse('api:talent:talent-list')
        #     talent_detail_url = reverse('api:talent:talent-detail')
        #     talent_detail_all_url = reverse('api:talent:talent-detail-all')
        #
        #     talent_list = self.client.get(talent_list_url)
        #     talent_detail = self.client.get(talent_detail_url)
        #     talent_detail_all = self.client.get(talent_detail_all_url)
        #
        #     self.assertEqual(talent_list.status_code, status.HTTP_200_OK)
        #     self.assertEqual(talent_detail_all.status_code, status.HTTP_200_OK)
        #     self.assertEqual(talent_detail.status_code, status.HTTP_200_OK)
