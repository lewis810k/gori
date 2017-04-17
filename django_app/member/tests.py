from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from utils import APITestUserLogin

User = get_user_model()


class UserSignUpLoginTest(APILiveServerTestCase, APITestUserLogin):
    test_user = 'test'
    test_password1 = 'testpw12'
    test_password2 = 'testpw12'
    test_name = 'testname'

    def test_signup(self):
        data = {
            'username': self.test_user,
            'password1': self.test_password1,
            'password2': self.test_password2,
            'name': self.test_name,
        }
        url = reverse('api:member:user-signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_obtain_token(self):
        user = self.create_user()
        self.assertEqual(User.objects.count(), 1)
        data = {
            'username': user.username,
            'password': 'testpw12',
        }
        url = reverse('api:member:user-token')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_login(self):
        user = self.create_user()
        self.assertEqual(User.objects.count(), 1)
        data = {
            'username': user.username,
            'password': 'testpw12',
        }
        url = reverse('api:member:rest_login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        token = self.test_obtain_token()
        self.assertEqual(User.objects.count(), 1)
        url = reverse('api:member:rest_logout')
        response = self.client.post(url, HTTP_AUTHORIZATION='Token ' + token.data.get('token'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MemberProfileTest(APILiveServerTestCase, APITestUserLogin):
    def test_user_detail_retrieve(self):
        user, token = self.obtain_token()
        url = reverse('api:member:user-detail')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user_id'), user.username)
        invalid_token = "asdf"
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token + invalid_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_update(self):
        user, token = self.obtain_token(1)
        patch_user_url = reverse('api:member:user-patch')
        new_nickname = "영나"
        new_name = "new_test_name"
        new_cellphone = "01099937576"
        data = {
            'nickname': new_nickname,
            "cellphone": new_cellphone,
            "name": new_name,
        }
        response = self.client.patch(patch_user_url, data=data, HTTP_AUTHORIZATION='Token ' + token)
        user = User.objects.get(username=user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.cellphone, new_cellphone)
        self.assertEqual(user.nickname, new_nickname)
        self.assertEqual(user.name, new_name)
        invalid_cellphone = "99djhjhgsdf32"
        invalid_data = [
            {"cellphone": invalid_cellphone, },
            {"nickname123": new_nickname, }, ]
        for item in invalid_data:
            response = self.client.patch(patch_user_url, item, HTTP_AUTHORIZATION='Token ' + token)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VerfiyFunctionTest(APILiveServerTestCase, APITestUserLogin):
    def test_staff_verify_tutor(self):
        users, tokens = self.obtain_token(2)
        tutor = self.create_tutor(users[1], tokens[1])
        params = {
            'tutor_pk': tutor.pk,
        }
        tutor_verify_url = reverse('api:member:tutor-verify', kwargs=params)
        response = self.client.get(tutor_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        users[0].is_staff = True
        users[0].save()
        response = self.client.get(tutor_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tutor.refresh_from_db()
        self.assertEqual(tutor.is_verified, True)
        response = self.client.get(tutor_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tutor.refresh_from_db()
        self.assertEqual(tutor.is_verified, False)
        params = {
            'tutor_pk': users[0].pk,
        }
        tutor_verify_url = reverse('api:member:tutor-verify', kwargs=params)
        response = self.client.get(tutor_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_verify_talent(self):
        users, tokens = self.obtain_token(2)
        tutor = self.create_tutor(users[1], tokens[1])
        talent = self.create_talent(tutor, tokens[1])
        params = {
            'talent_pk': talent.pk,
        }
        talent_verify_url = reverse('api:member:talent-verify', kwargs=params)
        response = self.client.get(talent_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        users[0].is_staff = True
        users[0].save()
        response = self.client.get(talent_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        talent.refresh_from_db()
        self.assertEqual(talent.is_verified, True)
        response = self.client.get(talent_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        talent.refresh_from_db()
        self.assertEqual(talent.is_verified, False)
        params = {
            'talent_pk': users[0].pk,
        }
        talent_verify_url = reverse('api:member:talent-verify', kwargs=params)
        response = self.client.get(talent_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tutor_verify_registration(self):
        users, tokens = self.obtain_token(2)
        tutor = self.create_tutor(users[0], tokens[0])
        talent = self.create_talent(tutor, tokens[0])
        location = self.create_location(talent, tokens[0])
        registration = self.create_registration(location, tokens[1])
        print(registration.talent_location.talent.tutor.pk)
        print(tutor.pk)

        talent.refresh_from_db()
        tutor.refresh_from_db()
        registration_verify_url = reverse('api:member:registration-verify',
                                          kwargs={"registration_pk": registration.pk})
        response = self.client.get(registration_verify_url,
                                   HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(registration_verify_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(registration_verify_url,
                                   HTTP_AUTHORIZATION='Token ' + tokens[1])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserWishlistTest(APILiveServerTestCase, APITestUserLogin):
    def test_user_wishlist_toggle(self):
        users, tokens = self.obtain_token(2)
        tutor = self.create_tutor(users[1], tokens[1])
        talent = self.create_talent(tutor, tokens[1])
        params = {
            'pk': talent.pk
        }
        wishlist_url = reverse('api:talent:wishlist-toggle', kwargs=params)
        response = self.client.get(wishlist_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(wishlist_url, HTTP_AUTHORIZATION='Token ' + tokens[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(wishlist_url, HTTP_AUTHORIZATION='Token ' + tokens[1])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_my_wishlist_view(self):
        pass
