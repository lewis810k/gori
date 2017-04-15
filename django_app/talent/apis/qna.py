from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from talent.models import Talent, Question, Reply
from talent.serializers import QuestionSerializer
from utils import verify_tutor, LargeResultsSetPagination

__all__ = (
    'QuestionListCreateView',
    'QuestionDeleteView',
    'ReplyCreateView',
)


class QuestionListCreateView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Question.objects.filter(talent_id=self.kwargs['pk'])

    def post(self, request):
        """

        필수정보 :
            - talent_pk : 수업 아이디
            - content : 질문 내용
        추가정보 :
        """
        try:
            talent_pk = request.data['talent_pk']
            user = request.user
            content = request.data['content']

            talent = Talent.objects.filter(pk=talent_pk).first()

            if not talent:
                ret = {
                    'detail': '수업({pk})이 존재하지 않습니다.'.format(pk=talent_pk)
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            # 자신의 수업이 아니어야 질문을 등록할 수 있음
            if not verify_tutor(request, talent):
                Question.objects.create(
                    talent=talent,
                    user=user,
                    content=content,
                )
                ret_message = '[{talent}]에 질문이 추가되었습니다.'.format(
                    talent=talent.title,
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

            # 자신의 수업에 질문을 등록하려는 경우
            else:
                ret = {
                    'detail': '자신의 수업에 질문을 등록할 수 없습니다.',
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        pk = request.data['pk']
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist as e:
            ret = {
                'detail': '질문[{}]이 존재하지 않습니다.'.format(pk)
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        # 지우려고 하는 question과 현재 유저가 같은지 확인
        if question.user == user:
            question.delete()
            ret_msg = '질문[{}]이 삭제되었습니다.'.format(pk)
            return_status = status.HTTP_200_OK
        else:
            ret_msg = '권한이 없습니다.'
            return_status = status.HTTP_400_BAD_REQUEST

        ret = {
            'detail': ret_msg,
        }
        return Response(ret, status=return_status)


class ReplyCreateView(APIView):
    queryset = Reply.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """

        필수정보 :
            - question_pk : 질문 아이디
            - content : 답변 내용
        추가정보 :
        """
        try:
            question_pk = request.data['question_pk']
            user = request.user
            content = request.data['content']
            question = Question.objects.filter(pk=question_pk).first()

            if not question:
                ret = {
                    'detail': '질문({pk})이 존재하지 않습니다.'.format(pk=question_pk)
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            # 이미 question이 존재하지 않으면 talent에 접근하지 못함
            # 여기서 에러가 발생하면 talent 지워질 때 question이 같이 지워지지 않은 것
            talent = question.talent

            # 자신의 수업이어야 답변을 등록할 수 있음
            if verify_tutor(request, talent):
                Reply.objects.create(
                    question=question,
                    tutor=user.tutor,
                    content=content,
                )
                ret_message = '질문[{pk}]에 댓글이 추가되었습니다.'.format(
                    pk=question_pk,
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

            # 자신의 수업이 아닌데 답변하려고 하거나 튜터가 아닌 경우
            else:
                ret = {
                    'detail': '권한이 없습니다.',
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
