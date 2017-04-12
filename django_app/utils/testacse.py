from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

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
