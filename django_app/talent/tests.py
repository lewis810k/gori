from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from member.models import GoriUser, Tutor
from talent.models import ClassImage
from talent.models import Talent



class GoriTest(APILiveServerTestCase):
    def test_create_user(self, num=1):
        user = []
        for i in range(num):
           user = GoriUser.objects.create_user(
                username='Gosunghyun{}'.format(i + 1),
                name='성현',
                password='votmxmzoa',
            )
        self.assertEqual(GoriUser.objects.count(), num)
        if num == 1:
            return user

    def test_create_tutor(self):
        user = self.test_create_user()
        tutor = Tutor.objects.create(
            user=user,
            is_verified=True,
            verification_method='UN',
            verification_images='E',
        )

        self.assertEqual(Tutor.objects.count(), 1)
        return tutor

    def test_create_talent(self):
        tutor = self.test_create_tutor()
        talent = Talent.objects.create(
            tutor=tutor,
            title='test',
            category='COM',
            type='0',
            cover_image='01.jpeg',
            tutor_info='test',
            class_info='test',
            price_per_hour='10000',
            hours_per_class='1000',
            number_of_class='10',
        )
        self.assertEqual(Talent.objects.count(), 1)
        return talent

    def test_create_class_image(self):
        talent = self.test_create_talent()
        class_image = ClassImage.objects.create(
            talent=talent,
            image='test01.jpeg'
        )
        self.assertEqual(ClassImage.objects.count(), 1)
        return class_image

    def test_talent_list_url_exist(self):
        url = 'http://127.0.0.1:8000/api/talent/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talent_detailall_url_exist(self):
        talent = self.test_create_talent()
        url = 'http://127.0.0.1:8000/api/talent/detail-all/{}/'.format(talent.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talent_detail_url_exist(self):
        talent = self.test_create_talent()
        url = 'http://127.0.0.1:8000/api/talent/detail/{}/'.format(talent.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_image_url_exist(self):
        # talent = self.test_create_talent()
        class_image = self.test_create_class_image()
        print(class_image.talent.pk)
        url = 'http://127.0.0.1:8000/api/talent/detail/{}/class-image/'.format(class_image.talent.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
