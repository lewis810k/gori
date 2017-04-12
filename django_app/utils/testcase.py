import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse

from member.models import Tutor
from talent.models import Talent, Location

User = get_user_model()


class APITest_User_Login(object):
    test_user = 'test'
    test_password1 = 'testpw12'
    test_password2 = 'testpw12'
    test_name = 'testname'

    def create_user_and_login(self):
        user = self.create_user()
        data = {
            'username': user.username,
            'password': 'testpw12',
        }
        url = reverse('api:member:rest_login')
        response = self.client.post(url, data, format='json')
        print(response)
        return user

    def obtain_token(self):
        user = self.create_user()
        data = {
            'username': user.username,
            'password': 'testpw12',
        }
        user_token_url = reverse('api:member:user-token')
        response = self.client.post(user_token_url, data, format='json')
        return user, response.data.get('token')

    def create_user(self):
        data = {
            'username': self.test_user,
            'password1': self.test_password1,
            'password2': self.test_password2,
            'name': self.test_name,
        }
        url = reverse('api: member:user - signup')
        self.client.post(url, data, format='json')
        user = User.objects.first()
        return user

    def create_tutor(self, user):
        file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
                                        content_type='image / jpeg')
        tutor = Tutor.objects.create(
            user=user,
            is_verified=True,
            verification_method='UN',
            verification_images=test_image
        )
        return tutor

    def create_talent(self, tutor):
        file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
                                        content_type='image / jpeg')
        talent = Talent.objects.create(
            tutor=tutor,
            title='test',
            category='COM',
            type='0',
            cover_image=test_image,
            tutor_info='test',
            class_info='test',
            price_per_hour='10000',
            hours_per_class='1000',
            number_of_class='10',
        )
        return talent

    def create_location(self, talent):
        location = Location.objects.create(
            talent=talent,
            region='KN',
            specific_location='NEGO',
            extra_fee='Y',
            day='MO',
            time='12시~16시'
        )
        return location
