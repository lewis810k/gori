from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.serializers import QuestionSerializer, QuestionCreateSerializer, ReplyCreateSerializer, \
    QuestionUpdateSerializer
from utils import *

__all__ = (
    'QuestionListCreateView',
    'QuestionDeleteView',
    'QuestionUpdateView',
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


class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionUpdateSerializer

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['pk'], user=self.request.user)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_queryset()
        if not instance.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "question_pk가 올바르지 않습니다"})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print(serializer)
        a = serializer.is_valid(raise_exception=True)
        serializer.save()
        # self.perform_update(serializer)
        return Response(status.HTTP_200_OK, data={"detail": "수정이 완료되었습니다!!"})
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     print('54324325342',instance)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)


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
