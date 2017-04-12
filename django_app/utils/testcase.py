from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()


class APITest_User_Login(object):
    test_user = 'test'
    test_password1 = 'testpw12'
    test_password2 = 'testpw12'
    test_name = 'testname'

    def create_user(self, num=1):
        users = []
        for i in range(num):
            user = User.objects.create_user(
                username='test_username{}'.format(i + 1),
                name='test{}'.format(i + 1),
                password='testpw12',
            )
            if num == 1:
                return user
            users.append(user)
        return users

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
        user = self.create_user(1)
        data = {
            'username': user.username,
            'password': 'testpw12',
        }
        user_token_url = reverse('api:member:user-token')
        response = self.client.post(user_token_url, data, format='json')
        return user, response.data.get('token')