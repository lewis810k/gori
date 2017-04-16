from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from talent.models import Talent, Question, Reply
from talent.serializers import QuestionSerializer, QuestionCreateSerializer, ReplyCreateSerializer
from utils import *

__all__ = (
    'QuestionListCreateView',
    'QuestionDeleteView',
    'ReplyCreateView',
    'ReplyDeleteView',
)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Question.objects.filter(talent_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        """
        필수정보 :
            - talent_pk : 수업 아이디
            - content : 질문 내용
        추가정보 :
        """
        request.data['user'] = request.user.id

        # 생성 전용 시리얼라이저 사용
        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ##### 추가 검증 절차 #####
        talent = Talent.objects.get(pk=request.data['talent_pk'])

        # ##### 자신의 수업이면 등록 불가능 #####
        if verify_tutor(request, talent):
            return Response(talent_owner_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 갯수 제한? #####

        # ##### 추가 검증 끝  #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)


class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['pk'], user=self.request.user)


class ReplyCreateView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        여기는 튜터 정보를 추출하기 위해서 verify_tutor를 먼저 실행한다.
        후에 is_valid 적용

        필수정보 :
            - question_pk : 질문 아이디
            - content : 답변 내용
        추가정보 :
        """
        request.data['user'] = request.user.id
        try:
            request.data['tutor'] = request.user.tutor
        except ObjectDoesNotExist as e:
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        # 생성 전용 시리얼라이저 사용
        serializer = ReplyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = Question.objects.get(pk=request.data['question_pk'])
        talent = question.talent

        # ##### 추가 검증 절차 #####
        # ##### 자신의 수업이 아니면 등록 불가능 #####
        if not verify_tutor(request, talent):
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 갯수 제한? #####

        # ##### 추가 검증 끝  #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)


class ReplyDeleteView(generics.DestroyAPIView):
    queryset = Reply.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Reply.objects.filter(pk=self.kwargs['pk'], tutor__user=self.request.user)
