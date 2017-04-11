from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from talent.models import Talent, Question
from talent.serializers import QnAWrapperSerializer
from utils import tutor_verify

__all__ = (
    'QnATalentRetrieveView',
    'QnACreateView',
)


class QnATalentRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = QnAWrapperSerializer


class QnACreateView(APIView):
    queryset = Question.objects.all()

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
            if not tutor_verify(request, talent):
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
