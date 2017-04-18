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

    # 여러개를 한번에 추가하려고 하는 경우. 이미지는 처리 불가
    def create_list(self, request):
        for data in request.data['input_list']:
            serializer = CurriculumCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            # ##### 추가 검증 절차 #####
            talent = Talent.objects.get(pk=data['talent_pk'])
            # ##### 자신의 수업이 아니면 등록 불가능 #####
            if not verify_tutor(request, talent):
                return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

            # ##### 추가 검증 끝  #####
            self.perform_create(serializer)

    def create(self, request, *args, **kwargs):
        """
        필수정보 :
            - talent_pk : 수업 아이디
            - information : 커리큘럼 설명
        추가정보 :
            - image : 커리큘럼 이미지
        """
        if 'input_list' in request.data:
            self.create_list(request)
        else:
            # 생성 전용 시리얼라이저 사용
            serializer = CurriculumCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # ##### 추가 검증 절차 #####
            talent = Talent.objects.get(pk=request.data['talent_pk'])

            # ##### 자신의 수업이 아니면 등록 불가능 #####
            if not verify_tutor(request, talent):
                return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

            # ##### 추가 검증 끝  #####

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED)


class CurriculumUpdateView(generics.UpdateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Curriculum.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)


class CurriculumDeleteView(generics.DestroyAPIView):
    queryset = Curriculum.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Curriculum.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)
