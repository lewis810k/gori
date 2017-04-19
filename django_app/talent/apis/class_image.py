from rest_framework import generics
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from talent.models import ClassImage
from talent.serializers import ClassImageSerializer, ClassImageCreateSerializer, ClassImageUpdateSerializer
from utils import *

__all__ = (
    'ClassImageListCreateView',
    'ClassImageDeleteView',
    'ClassImageUpdateView',
)


class ClassImageListCreateView(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (OrderingFilter,)
    ordering = ('-pk',)

    def get_queryset(self):
        return ClassImage.objects.filter(talent_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        """
        필수정보 :
            - talent_pk : 수업 아이디
            - image : 커리큘럼 이미지
        """
        # 생성 전용 시리얼라이저 사용
        serializer = ClassImageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ##### 추가 검증 절차 #####
        talent = Talent.objects.get(pk=request.data['talent_pk'])

        # ##### 자신의 수업이 아니면 등록 불가능 #####
        if not verify_tutor(request, talent):
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 갯수 제한? #####

        # ##### 추가 검증 끝  #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)


class ClassImageUpdateView(generics.UpdateAPIView):
    queryset = ClassImage.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClassImageUpdateSerializer

    def get_queryset(self):
        return ClassImage.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)


class ClassImageDeleteView(generics.DestroyAPIView):
    queryset = ClassImage.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ClassImage.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)
