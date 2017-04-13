from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from member.models import Tutor
from talent.models import ClassImage
from talent.models import Curriculum
from talent.models import Location
from talent.models import Question
from talent.models import Registration
from talent.models import Review
from talent.models import Talent
from utils import APITest_User_Login
from utils import image_upload


class GoriTest(APILiveServerTestCase, APITest_User_Login):
    def test_tutor_register(self):
        user = self.create_user()
        get_token = self.obtain_token(user)
        token = get_token
        test_image = image_upload()
        data = {
            'verification_method': 'UN',
            'verification_images': test_image,
            'school': 'test_university',
            'major': 'test_major',
            'current_status': 'E'
        }
        url = reverse('api:member:tutor-register')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutor.objects.count(), 1)
        return response, token

    def test_create_talent(self):
        test_image = image_upload()
        get_token = self.test_tutor_register()
        token = get_token[1]
        data = {
            'title': 'test_title',
            'category': 'COM',
            'type': 1,
            'tutor_info': 'test_info',
            'class_info': 'test_class_info',
            'number_of_class': 5,
            'price_per_hour': 20000,
            'hours_per_class': 2,
            'cover_image': test_image,
            'video1': 'test.com',
            'video2': 'test2.com'
        }
        url = reverse('api:talent:create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Talent.objects.count(), 1)
        talent = Talent.objects.first()
        return talent, token

    def test_create_curriculum(self):
        talent = self.test_create_talent()
        talent_pk = talent[0].pk
        token = talent[1]
        test_image = image_upload()
        data = {
            'talent_pk': talent_pk,
            'information': 'test_information',
            'image': test_image,
        }
        url = reverse('api:talent:curriculum-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curriculum.objects.count(), 1)

    def test_create_location(self):
        talent = self.test_create_talent()
        talent_pk = talent[0].pk
        token = talent[1]

        data = {
            'talent_pk': talent_pk,
            'region': 'EWWU',
            'specific_location': 'SELF',
            'day': 'MO',
            'time': '12~16시',
            'extra_fee': 'Y',
            'extra_fee_amount': 'extra',
            'location_info': 'location',
        }
        url = reverse('api:talent:location-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        location = Location.objects.first()
        return location, token

    def test_create_class_image(self):
        talent = self.test_create_talent()
        talent_pk = talent[0].pk
        token = talent[1]
        test_image = image_upload()
        data = {
            'talent_pk': talent_pk,
            'image': test_image
        }
        url = reverse('api:talent:class-image-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClassImage.objects.count(), 1)

    def test_registration_create(self):
        location = self.test_create_location()
        location_pk = location[0].pk
        user = self.create_user(2)
        token = self.obtain_token(user)
        data = {
            'location_pk': location_pk,
            'student_level': 3,
            'message_to_tutor': 'test_message'
        }
        url = reverse('api:talent:registration-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Registration.objects.count(), 1)

    def test_review_create(self):
        talent = self.test_create_talent()
        talent_pk = talent[0].pk
        user = self.create_user(2)
        token = self.obtain_token(user)
        data = {
            'talent_pk': talent_pk,
            'curriculum': 5,
            'readiness': 5,
            'timeliness': 5,
            'delivery': 5,
            'friendliness': 5,
            'comment': 'test'
        }
        url = reverse('api:talent:review-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_question_create(self):
        talent = self.test_create_talent()
        talent_pk = talent[0].pk
        user = self.create_user(2)
        token = self.obtain_token(user)

        data= {
            'talent_pk':talent_pk,
            'content':'test_comment'
        }
        url = reverse('api:talent:question-create')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

    def test_talent_list(self):
        """
        params : resgion:SD 은 사당으로 검색하기에
        :return:
        """
        #
        user = self.create_user()
        tutor = self.create_tutor(user)
        talent = self.create_talent(tutor)
        self.create_location(talent)
        params = {
            'region': 'SD'
        }
        url = reverse('api:talent:list')
        print(url)
        response = self.client.get(url, params)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 어떤 테스트인지
        params = {
            'title': 'test1'
        }
        response = self.client.get(url, params)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # def test_url_exist(self):
        #     talent = self.create_talent()
        #     talent_list_url = reverse('api:talent:talent-list')
        #     talent_detail_url = reverse('api:talent:talent-detail')
        #     talent_detail_all_url = reverse('api:talent:talent-detail-all')
        #
        #     talent_list = self.client.get(talent_list_url)
        #     talent_detail = self.client.get(talent_detail_url)
        #     talent_detail_all = self.client.get(talent_detail_all_url)
        #
        #     self.assertEqual(talent_list.status_code, status.HTTP_200_OK)
        #     self.assertEqual(talent_detail_all.status_code, status.HTTP_200_OK)
        #     self.assertEqual(talent_detail.status_code, status.HTTP_200_OK)
