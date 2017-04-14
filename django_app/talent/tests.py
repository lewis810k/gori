from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Registration, Location
from utils import APITest_User_Login

User = get_user_model()


class GoriTest(APILiveServerTestCase, APITest_User_Login):
    def test_token_create(self):
        # response = self.client.post(url, HTTP_AUTHORIZATION='Token ' + token.data.get('token'))

    def test_talent_create(self):
        token = self.create_user()
        data = {

        }

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


def test_url_exist(self):
    talent = self.create_talent()
    talent_list_url = reverse('api:talent:talent-list')
    talent_detail_url = reverse('api:talent:talent-detail')
    talent_detail_all_url = reverse('api:talent:talent-detail-all')
    talent_list = self.client.get(talent_list_url)
    talent_detail = self.client.get(talent_detail_url)
    talent_detail_all = self.client.get(talent_detail_all_url)
    self.assertEqual(talent_list.status_code, status.HTTP_200_OK)
    self.assertEqual(talent_detail_all.status_code, status.HTTP_200_OK)
    self.assertEqual(talent_detail.status_code, status.HTTP_200_OK)


class LocationCreateRetriveTest(APILiveServerTestCase, APITest_User_Login):
    def test_location_create(self):
        user, token = self.obtain_token()
        tutor = self.create_tutor(user, token)
        talent = self.create_talent(tutor, token)
        region = 'KN'
        day = "MO"
        time = "12-16,18-20"
        data = {
            "talent_pk": talent.pk,
            "region": region,
            "specific_location": 'NEGO',
            "extra_fee": 'Y',
            "day": day,
            "time": time,
        }
        url = reverse('api:talent:location-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.all().count(), 1)
        self.assertEqual(talent.locations.count(), 1)
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data["region"] = "JAU"
        self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(talent.locations.count(), 2)
        invalid_token = token + "##"
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + invalid_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data["talent_pk"] = 999
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        del data["talent_pk"]
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_location_retrieve(self):
        user, token = self.obtain_token()
        tutor = self.create_tutor(user, token)
        talent = self.create_talent(tutor, token)
        location = self.create_location(talent, token)
        valid_pk = talent.pk
        invalid_talent_pk = 999
        pk_s = [(valid_pk, status.HTTP_200_OK), (invalid_talent_pk, status.HTTP_404_NOT_FOUND)]
        for pk, expected_status_code in pk_s:
            params = {
                'pk': pk
            }
            location_retrieve_url = reverse('api:talent:location-retrieve', kwargs=params)
            response = self.client.get(location_retrieve_url)
            self.assertEqual(response.status_code, expected_status_code)
            if response.status_code == status.HTTP_200_OK:
                self.assertEqual(response.data["pk"], talent.pk)
                self.assertIn("locations", response.data)
                self.assertIn("region", response.data["locations"][0])
                self.assertIn("day", response.data["locations"][0])


class RegistrationCreateRetrieveTest(APILiveServerTestCase, APITest_User_Login):
    def test_registration_create(self):
        users, tokens = self.obtain_token(3)
        tutor = self.create_tutor(users[0], tokens[0])
        talent = self.create_talent(tutor, tokens[0])
        location = self.create_location(talent, tokens[0])
        message_to_tutor = "잘부탁드립니다"
        data = {
            "location_pk": location.pk,
            "student_level": 1,
            "message_to_tutor": message_to_tutor,
        }
        url = reverse('api:talent:registration-create')
        test_tokens = [(tokens[2] + '###', status.HTTP_401_UNAUTHORIZED),
                       ('', status.HTTP_401_UNAUTHORIZED),
                       (tokens[0], status.HTTP_400_BAD_REQUEST),
                       (tokens[1], status.HTTP_201_CREATED),
                       (tokens[1], status.HTTP_400_BAD_REQUEST), ]
        for token, expected_status_code in test_tokens:
            response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
            self.assertEqual(response.status_code, expected_status_code)
            if response.status_code == status.HTTP_201_CREATED:
                self.assertEqual(Registration.objects.get(student=users[1]).message_to_tutor, message_to_tutor)
                self.assertEqual(Registration.objects.filter(student=users[1]).count(), 1)
                self.assertEqual(Registration.objects.filter(talent_location=location).count(), 1)

    def test_registration_retrieve(self):
        users, tokens = self.obtain_token(4)
        tutor = self.create_tutor(users[0], tokens[0])
        talent = self.create_talent(tutor, tokens[0])
        location = self.create_location(talent, tokens[0])
        for index, token in enumerate(tokens[1:]):
            self.create_registration(location=location, token=token)
            registration_retrieve_url = reverse('api:talent:registration-retrieve', kwargs={'pk': talent.pk})
            response = self.client.get(registration_retrieve_url, HTTP_AUTHORIZATION='Token ' + token)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(str(Token.objects.get(key=token).user.pk),
                          response.data["registrations"][index]["message_to_tutor"])
            self.assertEqual(talent.title, response.data["title"])
        invalid_talent_pk = talent.pk + 1
        registration_retrieve_url = reverse('api:talent:registration-retrieve', kwargs={'pk': invalid_talent_pk})
        response = self.client.get(registration_retrieve_url, HTTP_AUTHORIZATION='Token ' + tokens[1])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
