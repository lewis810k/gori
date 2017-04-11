from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase


class GoriTest(APILiveServerTestCase):
    def create_post(self, num=1):
        # Post를 만들 유저를 생성 및 로그인

        url = reverse('api:post-list')
        for i in range(num):
            response = self.client.post(url)
            if num == 1:
                return response

    def test_url_exist(self):

        talent_list_url = reverse('api:talent:talent-list')
        talent_detail_url = reverse('api:talent:talent-detail')
        talent_detail_all_url = reverse('api:talent:talent-detail-all')

        talent_list = self.client.get(talent_list_url)
        talent_detail = self.client.get(talent_detail_url)
        talent_detail_all = self.client.get(talent_detail_all_url)

        self.assertEqual(talent_list.status_code, status.HTTP_200_OK)
        self.assertEqual(talent_detail_all.status_code, status.HTTP_200_OK)
        self.assertEqual(talent_detail.status_code, status.HTTP_200_OK)

    def test_talent_detailall_url_exist(self):
        talent = self.test_create_talent()
        url = 'http://127.0.0.1:8000/api/talent/detail-all/{}/'.format(talent.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_image_url_exist(self):
        # talent = self.test_create_talent()
        class_image = self.test_create_class_image()
        print(class_image.talent.pk)
        url = 'http://127.0.0.1:8000/api/talent/detail/{}/class-image/'.format(class_image.talent.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # def create_user(self, num=1):
        # users = []
        #     for i in range(num):
        #         user = GoriUser.objects.create_user(
        #             username='Gosunghyun{}'.format(i + 1),
        #             name='성현',
        #             password='votmxmzoa',
        #         )
        #         users.append(user)
        #     self.assertEqual(GoriUser.objects.count(), num)
        #     if num == 1:
        #         return user
        #
        # def create_user2(self, num=1):
        #     users = []
        #     for i in range(num):
        #         user = GoriUser.objects.create_user(
        #             username='Gosunghyun{}'.format(i + 1),
        #             name='성현',
        #             password='votmxmzoa',
        #         )
        #         users.append(user)
        #     self.assertEqual(GoriUser.objects.count(), num)
        #     if num == 1:
        #         return user
        #
        # def test_create_tutor(self):
        #     user = self.test_create_user()
        #     tutor = Tutor.objects.create(
        #         user=user,
        #         is_verified=True,
        #         verification_method='UN',
        #         verification_images='E',
        #     )
        #
        #     self.assertEqual(Tutor.objects.count(), 1)
        #     return tutor
        #
        # def test_create_talent(self):
        #     tutor = self.test_create_tutor()
        #     file_path = os.path.dirname(os.path.abspath(__file__))
        #     test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
        #                                         content_type='image/jpeg')
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
        #     self.assertEqual(Talent.objects.count(), 1)
        #     return talent
        #
        # def test_create_class_image(self):
        #     talent = self.test_create_talent()
        #     file_path = os.path.dirname(os.path.abspath(__file__))
        #     test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
        #                                     content_type='image/jpeg')
        #     class_image = ClassImage.objects.create(
        #         talent=talent,
        #         image=test_image,
        #     )
        #     self.assertEqual(ClassImage.objects.count(), 1)
        #     return class_image
        # def test_create_location(self):
        #     talent = self.test_create_talent()
        #
        #     location = Location.objects.create(
        #         talent=talent,
        #         region='KN',
        #         specific_location='NEGO',
        #         extra_fee='N',
        #         day='MO',
        #         time='12시~16시'
        #     )
