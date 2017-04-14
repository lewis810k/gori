from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Question
from utils import APITest_User_Login


# class TutorTest(APILiveServerTestCase, APITest_User_Login):
#     def test_tutor_register(self):
#         """
#         유저를 tutor로 등록시키는 코드
#         :return:
#         """
#         user, token = self.obtain_token(2)
#         token = token[0]
#         user_token = token[1]
#         test_image = image_upload()
#         data = {
#             'verification_method': 'UN',
#             'verification_images': test_image,
#             'school': 'test_university',
#             'major': 'test_major',
#             'current_status': 'E'
#         }
#         fail_data = {
#             'verification_method': 'ZX',
#             'verification_images': test_image,
#             'school': 'test_university',
#             'major': 'test_major',
#             'current_status': 'E'
#         }
#         url = reverse('api:member:tutor-register')
#         response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + token)
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Tutor.objects.count(), 1)
#         response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + token)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class TalentCreatTest(APILiveServerTestCase, APITest_User_Login):
#     def test_create_talent(self):
#         test_image = image_upload()
#         user, user_token = self.obtain_token(2)
#         tutor = self.register_tutor(user[0], user_token[0])
#         data = {
#             'title': 'test',
#             'category': 'COM',
#             'type': 1,
#             'tutor_info': 'test_info',
#             'class_info': 'test_class_info',
#             'number_of_class': 5,
#             'price_per_hour': 20000,
#             'hours_per_class': 2,
#             'cover_image': test_image,
#             'video1': 'test.com',
#             'video2': 'test2.com'
#         }
#         fail_data = {
#             'title': 'test1',
#             'category': 'COM',
#             'type': 1,
#             'tutor_info': 'test_info',
#             'class_info': 'test_class_info',
#             'number_of_class': 5,
#             'hours_per_class': 2,
#             'cover_image': test_image,
#             'video1': 'test.com',
#             'video2': 'test2.com'
#         }
#         title_overlap_fail_data = {
#             'title': 'test',
#             'category': 'COM',
#             'type': 1,
#             'tutor_info': 'test_info',
#             'class_info': 'test_class_info',
#             'number_of_class': 5,
#             'price_per_hour': 20000,
#             'hours_per_class': 2,
#             'cover_image': test_image,
#             'video1': 'test.com',
#             'video2': 'test2.com'
#         }
#         url = reverse('api:talent:create')
#         response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Talent.objects.count(), 1)
#         response = self.client.post(url, fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(url, title_overlap_fail_data, HTTP_AUTHORIZATION='Token ' + user_token[0])
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + user_token[1])
#
#
# class TalentTest(APILiveServerTestCase, APITest_User_Login):
#     def test_talent_list(self):
#         """
#         params : resgion:SD 은 사당으로 검색하기에
#         :return:
#         """
#         #
#         user, user_token = self.obtain_token()
#         tutor = self.register_tutor(user, user_token)
#         talent = self.create_talent(tutor, user_token)
#         location = self.create_location(talent, user_token)
#         url = reverse('api:talent:list')
#         response = self.client.get(url)
#         field_list = ['pk', 'title', 'category', 'type', 'tutor', 'tutor', 'user_id', 'name', 'nickname', 'is_verified',
#                       'profile_image', 'cellphone', 'is_school', 'cover_image', 'price_per_hour', 'hours_per_class',
#                       'number_of_class', 'min_number_student', 'max_number_student', 'is_soldout', 'created_date',
#                       'average_rate', 'review_count', 'registration_count', 'regions']
#         response_list = list(response.data[0].keys()) + list(response.data[0]["tutor"])
#
#         for field in field_list:
#             self.assertIn(field, response_list)
#
#         params_list = [
#             ({'region': 'KN'}, 1),
#             ({'region': 'SD'}, 0),
#             ({'title': 'test'}, 1),
#             ({'title': 'qwer'}, 0),
#             ({'category': 'COM'}, 1),
#             ({'category': 'SPO'}, 0),
#         ]
#         url = reverse('api:talent:list')
#         for param_item in params_list:
#             response = self.client.get(url, param_item[0])
#             self.assertEqual(len(response.data), param_item[1])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_talent_detail_retrieve_all_url_exist(self):
#         user, user_token = self.obtain_token()
#         tutor = self.register_tutor(user, user_token)
#         talent = self.create_talent(tutor, user_token)
#         url = reverse('api:talent:detail-all', kwargs={'pk': talent.pk})
#         response = self.client.get(url)
#         field_list = ['pk', 'title', 'category', 'type', 'tutor', 'tutor', 'user_id', 'name', 'nickname', 'is_verified',
#                       'profile_image', 'cellphone', 'cover_image', 'price_per_hour', 'hours_per_class',
#                       'number_of_class', 'min_number_student', 'max_number_student',
#                       'average_rate', 'review_count']
#         # 'registration_count', 모델다시 해놓고 바꿔줄것
#         response_list = list(response.data) + list(response.data["tutor"])
#
#         for field in field_list:
#             self.assertIn(field, response_list)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         url = reverse('api:talent:detail-all', kwargs={'pk': 999})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_talent_detail_short_retrieve_url_exist(self):
#         user, user_token = self.obtain_token()
#         tutor = self.register_tutor(user, user_token)
#         talent = self.create_talent(tutor, user_token)
#         url = reverse('api:talent:detail-short', kwargs={'pk': talent.pk})
#         response = self.client.get(url)
#         field_list = ['max_number_student', 'price_per_hour', 'is_verified', 'category', 'number_of_class',
#                       'hours_per_class', 'is_soldout', 'class_info', 'video1', 'video2', 'pk', 'title', 'tutor',
#                       'user_id', 'name', 'nickname', 'profile_image', 'cellphone', 'type', 'cover_image',
#                       'tutor_info', 'average_rate', 'review_count', 'min_number_student']
#         response_list = list(response.data) + list(response.data["tutor"])
#
#         for field in field_list:
#             self.assertIn(field, response_list)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         url = reverse('api:talent:detail-all', kwargs={'pk': 999})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class CurriculumCreateTest(APILiveServerTestCase, APITest_User_Login):
#     def test_create_curriculum(self):
#         user, user_token = self.obtain_token(2)
#         tutor = self.register_tutor(user[0], user_token[0])
#         talent = self.create_talent(tutor, user_token[0])
#         test_image = image_upload()
#         data = {
#             'talent_pk': talent.pk,
#             'information': 'test_information',
#             'image': test_image,
#         }
#         url = reverse('api:talent:curriculum-create')
#         response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('detail', response.data)
#         fail_list = [
#             ['talent_pk', 555],
#             ["", ""]
#         ]
#         for fail_item in fail_list:
#             fail_data = {
#                 fail_item[0]: fail_item[1],
#                 'information': 'test_information',
#                 'image': test_image,
#             }
#             url = reverse('api:talent:curriculum-create')
#             response = self.client.post(url, fail_data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[0])
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             if fail_item[0] == "":
#                 self.assertIn('non_field_error', response.data)
#             else:
#                 self.assertIn('detail', response.data)
#         fail_token = [
#             user_token[1],
#             ""
#         ]
#         for fail_item in fail_token:
#             url = reverse('api:talent:curriculum-create')
#             response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + fail_item)
#             self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class CurriculumRetrieveTest(APILiveServerTestCase, APITest_User_Login):
#     def test_curriculum_retrieve_url_exist(self):
#         user, user_token = self.obtain_token()
#         tutor = self.register_tutor(user, user_token)
#         talent = self.create_talent(tutor, user_token)
#         curriculum = self.create_curriculum(talent, user_token)
#
#         url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': talent.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         response_list = list(response.data) + list(response.data['curriculums'][0])
#         field_list = ['pk', 'title', 'category', 'type', 'curriculums', 'talent_pk', 'information', 'image']
#         for field_item in field_list:
#             self.assertIn(field_item, response_list)
#         url = reverse('api:talent:curriculum-retrieve', kwargs={'pk': 123})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class ReviewCreateTest(APILiveServerTestCase, APITest_User_Login):
#     def test_create_review(self):
#         user, user_token = self.obtain_token(2)
#         tutor = self.register_tutor(user[0], user_token[0])
#         talent = self.create_talent(tutor, user_token[0])
#         fail_list = [
#             [1234, 'readiness', user_token[1]],
#             [talent.pk, '', user_token[1]],
#             [talent.pk, 'readiness', user_token[0]],
#             [talent.pk, 'readiness', user_token[1]],
#             [talent.pk, 'readiness', ""],
#         ]
#         for fail_item in fail_list:
#             data = {
#                 'talent_pk': fail_item[0],
#                 'curriculum': 5,
#                 fail_item[1]: 5,
#                 'timeliness': 5,
#                 'delivery': 5,
#                 'friendliness': 5,
#                 'comment': 'test_comment'
#             }
#             url = reverse('api:talent:review-create')
#             response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + fail_item[2])
#             if fail_item[1] == "":
#                 self.assertIn('non_field_error', response.data)
#                 self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             elif fail_item[0] == talent.pk and fail_item[1] == 'readiness' and fail_item[2] == user_token[1]:
#                 self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#                 self.assertEqual(Review.objects.count(), 1)
#             elif fail_item[2] == "":
#                 self.assertIn('detail', response.data)
#                 self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#             else:
#                 self.assertIn('detail', response.data)
#                 self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION='Token ' + user_token[1])
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Review.objects.count(), 1)

class ReviewRetrieveTest(APILiveServerTestCase, APITest_User_Login):
    def test_review_retrieve_url_exist(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        review = self.create_review(talent, user_token[1])

        url = reverse('api:talent:review-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)
        response_list = list(response.data) + list(response.data['reviews'][0]) \
                        + list(response.data['reviews'][0]['user'])
        field_list = ['pk', 'title', 'category', 'type', 'average_rates', 'review_count', 'reviews', 'talent', 'user',
                      'curriculum', 'readiness', 'timeliness', 'delivery', 'friendliness', 'created_date', 'comment',
                      'name', 'profile_image']

        for field_item in field_list:
            self.assertIn(field_item, response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:talent:review-retrieve', kwargs={'pk': 555})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class QuestionCreatTest(APILiveServerTestCase, APITest_User_Login):
    def test_create_question(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])

        test_list = [
            [555, "content", user_token[1]],
            [talent.pk, "", user_token[1]],
            [talent.pk, 'content', user_token[0]],
            [talent.pk, 'content', ""],
            [talent.pk, 'content', user_token[1]],
        ]
        for test_item in test_list:
            data = {
                'talent_pk': test_item[0],
                test_item[1]: 'test_content'
            }
            url = reverse('api:talent:question-create')
            response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + test_item[2])
            if test_item[0] == talent.pk and test_item[1] == 'content' and test_item[2] == user_token[1]:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(Question.objects.count(), 1)
            elif test_item[2] == '':
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertIn('detail', response.data)
            elif test_item[1] == '':
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('non_field_error', response.data)
            else:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('detail', response.data)


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
