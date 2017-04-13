import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse

from member.models import Tutor
from talent.models import Talent, Location
from utils.upload import image_upload

User = get_user_model()


class APITest_User_Login(object):
    test_user = 'test{}'
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
        return user

    def create_user(self, number=1):
        users = []
        for i in range(number):
            username = self.test_user.format(i)
            data = {
                'username': username,
                'password1': self.test_password1,
                'password2': self.test_password2,
                'name': self.test_name,
            }
            url = reverse('api:member:user-signup')
            response = self.client.post(url, data, format='json')
            user = User.objects.get(username=username)
            if number == 1:
                return user
            users.append(user)
        return users

    def obtain_token(self, number=1):
        tokens = []
        users = self.create_user(number)
        if number == 1:
            data = {
                'username': users.username,
                'password': 'testpw12',
            }
            user_token_url = reverse('api:member:user-token')
            response = self.client.post(user_token_url, data, format='json')
            return users, response.data.get('token')
        for user in users:
            data = {
                'username': user.username,
                'password': 'testpw12',
            }
            user_token_url = reverse('api:member:user-token')
            response = self.client.post(user_token_url, data, format='json')
            # if number ==1:
            #     return user, response.data.get('token')
            tokens.append(response.data.get('token'))

        return users, tokens

    # def create_tutor(self, user):
    #     file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    #     test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
    #                                     content_type='image/jpeg')
    #     tutor = Tutor.objects.create(
    #         user=user,
    #         is_verified=True,
    #         verification_method='UN',
    #         verification_images=test_image
    #     )
    #     return tutor

    def register_tutor(self, user, token=None):
        # file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        # test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
        #                                 content_type='image/jpeg')
        test_image = image_upload()
        data = {
            "user": user,
            "is_verified": True,
            "verification_method": 'UN',
            "verification_images": test_image
        }
        tutor_create_url = reverse('api:member:tutor-register')
        response = self.client.post(tutor_create_url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + token)
        tutor = Tutor.objects.get(user=user)
        return tutor

    # def create_talent(self, tutor):
    #     file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    #     test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
    #                                     content_type='image / jpeg')
    #     talent = Talent.objects.create(
    #         tutor=tutor,
    #         title='test',
    #         category='COM',
    #         type='0',
    #         cover_image=test_image,
    #         tutor_info='test',
    #         class_info='test',
    #         price_per_hour='10000',
    #         hours_per_class='1000',
    #         number_of_class='10',
    #     )
    #     return talent

    def create_talent(self, tutor, token=None):
        file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
                                        content_type='image / jpeg', )
        data = {
            'tutor': tutor,
            'title': 'test',
            'category': 'COM',
            'type': '0',
            'cover_image': test_image,
            'tutor_info': 'test',
            'class_info': 'test',
            'price_per_hour': '10000',
            'hours_per_class': '1000',
            'number_of_class': '10',

        }
        url = reverse('api:talent:create')
        print(url)
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + token)
        talent = Talent.objects.last()
        return talent

    def create_location(self, talent, token=None):
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
        print(response.data)
        location = Location.objects.get(region=region, day=day, time=time)
        return location