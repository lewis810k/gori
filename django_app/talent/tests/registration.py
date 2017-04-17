from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Registration
from utils import APITestUserLogin

User = get_user_model()

class RegistrationCreateRetrieveTest(APILiveServerTestCase, APITestUserLogin):
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
        tutor = self.register_tutor(users[0], tokens[0])
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
