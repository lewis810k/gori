from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from member.models import Tutor
from talent.models import Talent
from utils import APITest_User_Login
from utils.upload import image_upload


class TutorTest(APILiveServerTestCase, APITest_User_Login):
    def test_tutor_register(self):
        """
        유저를 tutor로 등록시키는 코드
        :return:
        """
        user, token = self.obtain_token(2)
        token = token[0]
        user_token = token[1]
        test_image = image_upload()
        data = {
            'verification_method': 'UN',
            'verification_images': test_image,
            'school': 'test_university',
            'major': 'test_major',
            'current_status': 'E'
        }
        fail_data = {
            'verification_method': 'ZX',
            'verification_images': test_image,
            'school': 'test_university',
            'major': 'test_major',
            'current_status': 'E'
        }
        url = reverse('api:member:tutor-register')
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + token)
        self.assertIn('detail', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutor.objects.count(), 1)
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TalentCreatTest(APILiveServerTestCase, APITest_User_Login):
    def test_create_talent(self):
        test_image = image_upload()
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        data = {
            'title': 'test',
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
        fail_data = {
            'title': 'test1',
            'category': 'COM',
            'type': 1,
            'tutor_info': 'test_info',
            'class_info': 'test_class_info',
            'number_of_class': 5,
            'hours_per_class': 2,
            'cover_image': test_image,
            'video1': 'test.com',
            'video2': 'test2.com'
        }
        title_overlap_fail_data = {
            'title': 'test',
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
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertIn('detail', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Talent.objects.count(), 1)
        response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, title_overlap_fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token[1])


class TalentTest(APILiveServerTestCase, APITest_User_Login):
    def test_talent_list(self):
        """
        params : resgion:SD 은 사당으로 검색하기에
        :return:
        """
        #
        user, user_token = self.obtain_token()
        tutor = self.register_tutor(user, user_token)
        talent = self.create_talent(tutor, user_token)
        location = self.create_location(talent, user_token)
        url = reverse('api:talent:list')
        response = self.client.get(url)
        field_list = ['pk', 'title', 'category', 'type', 'tutor', 'tutor', 'user_id', 'name', 'nickname', 'is_verified',
                      'profile_image', 'cellphone', 'is_school', 'cover_image', 'price_per_hour', 'hours_per_class',
                      'number_of_class', 'min_number_student', 'max_number_student', 'is_soldout', 'created_date',
                      'average_rate', 'review_count', 'registration_count', 'regions']
        # self.assertIn(['pk'],response.data)
        # talent_key = Talent.objects.first()
        response_list = list(response.data[0].keys())+list(response.data[0]["tutor"])
        list1 = list(response.data[0].keys())
        list2 = list(response.data[0]["tutor"])
        list1.extend(list2)
        print(list1)
        print(list2)
        print(response_list)

        for field in field_list:
            self.assertIn(field,response_list)

        params_list = [
            ({'region': 'KN'}, 1),
            ({'region': 'SD'}, 0),
            ({'title': 'test'}, 1),
            ({'title': 'qwer'}, 0),
            ({'category': 'COM'}, 1),
            ({'category': 'SPO'}, 0),
        ]
        url = reverse('api:talent:list')
        for param_item in params_list:
            response = self.client.get(url, param_item[0])
            self.assertEqual(len(response.data), param_item[1])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talent_detail_retrieve_all_url_exist(self):
        talent = Talent.objects.first()
        print('talnet{}'.format(talent.title))
        # def test_create_curriculum(self):
        #     talent = self.test_create_talent()
        #     talent_pk = talent[0].pk
        #     token = talent[1]
        #     test_image = image_upload()
        #     data = {
        #         'talent_pk': talent_pk,
        #         'information': 'test_information',
        #         'image': test_image,
        #     }
        #     url = reverse('api:talent:curriculum-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Curriculum.objects.count(), 1)
        #
        # def test_create_location(self):
        #     talent = self.test_create_talent()
        #     talent_pk = talent[0].pk
        #     token = talent[1]
        #
        #     data = {
        #         'talent_pk': talent_pk,
        #         'region': 'EWWU',
        #         'specific_location': 'SELF',
        #         'day': 'MO',
        #         'time': '12~16시',
        #         'extra_fee': 'Y',
        #         'extra_fee_amount': 'extra',
        #         'location_info': 'location',
        #     }
        #     url = reverse('api:talent:location-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Location.objects.count(), 1)
        #     location = Location.objects.first()
        #     return location, token
        #
        # def test_create_class_image(self):
        #     talent = self.test_create_talent()
        #     talent_pk = talent[0].pk
        #     token = talent[1]
        #     test_image = image_upload()
        #     data = {
        #         'talent_pk': talent_pk,
        #         'image': test_image
        #     }
        #     url = reverse('api:talent:class-image-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(ClassImage.objects.count(), 1)
        #
        # def test_create_registration(self):
        #     location = self.test_create_location()
        #     location_pk = location[0].pk
        #     user = self.create_user(2)
        #     token = self.obtain_token(user)
        #     data = {
        #         'location_pk': location_pk,
        #         'student_level': 3,
        #         'message_to_tutor': 'test_message'
        #     }
        #     url = reverse('api:talent:registration-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Registration.objects.count(), 1)
        #
        # def test_create_review(self):
        #     talent = self.test_create_talent()
        #     talent_pk = talent[0].pk
        #     user = self.create_user(2)
        #     token = self.obtain_token(user)
        #     data = {
        #         'talent_pk': talent_pk,
        #         'curriculum': 5,
        #         'readiness': 5,
        #         'timeliness': 5,
        #         'delivery': 5,
        #         'friendliness': 5,
        #         'comment': 'test'
        #     }
        #     url = reverse('api:talent:review-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Review.objects.count(), 1)
        #
        # def test_create_question(self):
        #     talent = self.test_create_talent()
        #     talent_pk = talent[0].pk
        #     user = self.create_user(2)
        #     token = self.obtain_token(user)
        #
        #     data = {
        #         'talent_pk': talent_pk,
        #         'content': 'test_comment'
        #     }
        #     url = reverse('api:talent:question-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Question.objects.count(), 1)
        #     question = Question.objects.first()
        #     return question
        #
        # def test_create_reply(self):
        #     tutor = self.test_tutor_register()
        #     question = self.test_create_question()
        #     question_pk = question.pk
        #     token = tutor[1]
        #     print('토큰{}'.format(token))
        #     data = {
        #         'question_pk': question_pk,
        #         'content': 'test_content'
        #     }
        #     url = reverse('api:talent:reply-create')
        #     response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + token)
        #     print('이게뭘까{}'.format(response.data))
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Reply.objects.count(), 1)
        #
        # def test_talent_list(self):
        #     """
        #     params : resgion:SD 은 사당으로 검색하기에
        #     :return:
        #     """
        #     #
        #     user = self.create_user()
        #     tutor = self.create_tutor(user)
        #     talent = self.create_talent(tutor)
        #     self.create_location(talent)
        #     params = {
        #         'region': 'SD'
        #     }
        #     url = reverse('api:talent:list')
        #     print(url)
        #     response = self.client.get(url, params)
        #     self.assertEqual(len(response.data), 0)
        #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        #
        #     # 어떤 테스트인지
        #     params = {
        #         'title': 'test1'
        #     }
        #     response = self.client.get(url, params)
        #     self.assertEqual(len(response.data), 0)
        #     self.assertEqual(response.status_code, status.HTTP_200_OK)
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
