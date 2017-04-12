import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse

from member.models import Tutor

User = get_user_model()

class APITest_User_Login(object):
    test_user = 'test'
    test_password1 = 'qwer1234'
    test_password2 = 'qwer1234'
    test_name = 'testname'

    def create_user(self, num=1):
        users = []
        for i in range(num):
            user = User.objects.create_user(
                username='test_username{}'.format(i + 1),
                name='test{}'.format(i + 1),
                password='votmxmzoa',
            )
            users.append(user)
        if num == 1:
            return user

    def create_user_and_login(self):
        user = self.create_user()
        data = {
            'username': user.username,
            'password': 'votmxmzoa',
        }
        url = reverse('api:member:rest_login')
        response = self.client.post(url, data, format='json')
        print(response)
        return user

    def create_totur(self):
        user = self.create_user()
        file_path = os.path.dirname(os.path.abspath(__file__))
        test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
                                            content_type='image/jpeg')
        tutor = Tutor.objects.create(
            uesr=user,
            is_verified=True,
            verification_method='UN',
            verification_images=test_image
        )
