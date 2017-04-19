from __future__ import unicode_literals

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from talent.serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from utils import *

__all__ = (
    'ReviewListCreateView',
    'ReviewDeleteView',
    'ReviewUpdateView',
)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering = ('-pk',)

    def get_queryset(self):
        return Review.objects.filter(talent_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        """
        특정 수업에 대해 리뷰를 작성한다.
        자신의 수업에 대해서는 리뷰를 작성할 수 없도록 한다.

        수강생만 리뷰 등록 가능!

        필수정보 :
            - talent_pk : 수업 아이디
        추가정보 :
            - (점수들은 default=1을 가짐)
            - curriculum : 커리큘럼에 대한 점수
            - readiness : 준비성에 대한 점수
            - timeliness : 시간을 잘 지켰는지에 대한 점수
            - delivery : 전달력에 대한 점수
            - friendliness : 친근감?에 대한 점수
            - comment : 코멘트
        """
        request.data['user'] = request.user.id
        print("=====================")

        # 생성 전용 시리얼라이저 사용
        print('---------before serializer-------')
        serializer = ReviewCreateSerializer(data=request.data)
        print('---------before is_valid---------')
        serializer.is_valid(raise_exception=True)
        print('---------after is_valid--------')
        # ##### 추가 검증 절차 #####
        talent = Talent.objects.get(pk=request.data['talent_pk'])

        # ##### 자신의 수업이면 등록 불가능 #####
        if verify_tutor(request, talent):
            return Response(talent_owner_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 이미 리뷰가 존재하면 등록 불가능#####
        # data = {
        #     'talent': talent,
        #     'user': request.user,
        # }
        # if verify_duplicate(Review, data=data):
        #     return Response(multiple_item_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 추가 검증 끝  #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)


class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReviewUpdateSerializer

    def get_queryset(self):
        return Review.objects.filter(pk=self.kwargs['pk'], user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_200_OK, data=success_update)


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Review.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
