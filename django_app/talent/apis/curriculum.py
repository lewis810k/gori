from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.serializers import CurriculumSerializer, CurriculumUpdateSerializer
from talent.serializers.curriculum import CurriculumCreateSerializer
from utils import *

__all__ = (
    'CurriculumListCreateView',
    'CurriculumDeleteView',
    'CurriculumUpdateView',
)


class CurriculumListCreateView(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Curriculum.objects.filter(talent_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        """
        필수정보 :
            - talent_pk : 수업 아이디
            - information : 커리큘럼 설명
        추가정보 :
            - image : 커리큘럼 이미지
        """
        # 생성 전용 시리얼라이저 사용
        serializer = CurriculumCreateSerializer(data=request.data)
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


class CurriculumUpdateView(generics.UpdateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Curriculum.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)

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


class CurriculumDeleteView(generics.DestroyAPIView):
    queryset = Curriculum.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Curriculum.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)
