from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APILiveServerTestCase

from talent.models import Question
from utils import APITestUserLogin

User = get_user_model()

__all__ = (
    'QuestionCreateTest',
    'ReplyCreateTest',
    'QnARetrieveTest',
)


class QuestionCreateTest(APILiveServerTestCase, APITestUserLogin):
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


class ReplyCreateTest(APILiveServerTestCase, APITestUserLogin):
    def test_create_reply(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        question = self.create_question(talent, user_token[1])

        test_list = [
            [555, "content", user_token[0]],
            [question.pk, "", user_token[0]],
            [question.pk, 'content', user_token[1]],
            [question.pk, 'content', ""],
            [question.pk, 'content', user_token[0]],
        ]
        for test_item in test_list:
            data = {
                'question_pk': test_item[0],
                test_item[1]: 'test_content'
            }
            url = reverse('api:talent:reply-create')
            response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + test_item[2])
            if test_item[0] == question.pk and test_item[1] == 'content' and test_item[2] == user_token[0]:
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


class QnARetrieveTest(APILiveServerTestCase, APITestUserLogin):
    def test_qna_retrieve_url_exist(self):
        user, user_token = self.obtain_token(2)
        tutor = self.register_tutor(user[0], user_token[0])
        talent = self.create_talent(tutor, user_token[0])
        question = self.create_question(talent, user_token[1])
        reply = self.create_reply(question, user_token[0])

        url = reverse('api:talent:qna-retrieve', kwargs={'pk': talent.pk})
        response = self.client.get(url)

