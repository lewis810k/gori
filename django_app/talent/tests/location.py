from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Location
from utils import APITestUserLogin, get_user_model

User = get_user_model()


class LocationCreateRetriveTest(APILiveServerTestCase, APITestUserLogin):

    def test_location_create(self):
        user, token = self.obtain_token()
        tutor = self.register_tutor(user, token)
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
        tutor = self.register_tutor(user, token)
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