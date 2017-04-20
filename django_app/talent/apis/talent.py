from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
from talent.serializers import TalentDetailSerializer, TalentCreateSerializer, TalentUpdateSerializer
from talent.serializers import TalentListSerializer, TalentShortDetailSerializer
from utils import *

__all__ = (
    'TalentListCreateView',
    'UnverifiedTalentListView',
    # detail - all
    'TalentDetailView',
    # detail - fragments
    'TalentShortDetailView',
    'TalentSalesStatusToggleView',
    'TalentDeleteView',
    'TalentUpdateView'
)

User = get_user_model()


# talent 전체 api
class TalentListCreateView(generics.ListCreateAPIView):
    serializer_class = TalentListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (OrderingFilter,)
    ordering = ('-pk',)

    # rest_framework의 SearchFilter 사용시
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('title', 'class_info')

    def create(self, request, *args, **kwargs):
        """
        필수정보 :
            - title : 수업 제목
            - category : 카테고리
            - type : 수업 형태
            - cover_image : 수업 이미지
            - tutor_info : 튜터 자기소개
            - class_info : 수업 소개
            - number_of_class : 한달기준 수업횟수
            - price_per_hour : 시간당 금액
            - hours_per_class : 회당 수업시간
        추가정보 :
            - video1 : 비디오링크 1
            - video2 : 비디오링크 2
            - min_number_student : 최소 인원수
            - max_number_student : 최대 인원수
            - tutor_message : 튜터 메시지

        """
        user = request.user
        request.data['user'] = user.id
        # 요청하는 유저가 튜터인지 체크
        try:
            request.data['tutor'] = request.user.tutor
        except ObjectDoesNotExist as e:
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        # 생성 전용 시리얼라이저 사용
        serializer = TalentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ##### 추가 검증 절차 #####

        # 이미 같은 이름의 수업이 존재하면 400 리턴
        data = {
            'title': request.data['title'],
        }
        if verify_duplicate(Talent, data):
            return Response(title_already_exist, status=status.HTTP_400_BAD_REQUEST)
        # ##### 추가 검증 끝  #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        ret_pk = {
            "talent_pk": Talent.objects.filter(title=serializer.data['title']).first().pk,
        }
        ret = success_msg.copy()
        ret.update(ret_pk)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Talent.objects.all()
        title = self.request.query_params.get('title', None)
        region = self.request.query_params.get('region', None)
        category = self.request.query_params.get('category', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if region is not None:
            queryset = queryset.filter(locations__region__icontains=region).distinct('pk')
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        queryset = queryset.filter(is_verified=True)
        return queryset


# 인증 승인이 필요한 talent list api
class UnverifiedTalentListView(generics.ListAPIView):
    permission_classes = (custom_permission.CustomerIsAdminAccessPermission,)
    queryset = Talent.objects.filter(is_verified=False)
    serializer_class = TalentListSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (OrderingFilter,)
    ordering = ('-pk',)


class TalentShortDetailView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentShortDetailSerializer


# 하나의 talent에 대한 세부 정보 api (request user 정보 포함)
class TalentDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            talent = Talent.objects.get(pk=kwargs['pk'])
            talent_dict = TalentDetailSerializer(talent).data
            user = request.user
            try:
                user_dict = UserSerializer(user).data
                talent_dict["user"] = user_dict
            except:
                talent_dict["user"] = "Login Required"

            return Response(talent_dict)
        except Talent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "찾을 수 없습니다."})


# talent의 is_soldout 상태 toggle
class TalentSalesStatusToggleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        if hasattr(user, 'tutor'):
            tutor = request.user.tutor
            try:
                talent = Talent.objects.get(pk=pk)
                if talent in tutor.talent_set.all():
                    talent, detail = switch_sales_status(pk)
                    return Response(status=status.HTTP_200_OK,
                                    data={"detail": detail})
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "해당 요청에 대한 권한이 없습니다."})
            except Talent.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "해당 수업 내역을 찾을 수 없습니다."})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "해당 요청에 대한 권한이 없습니다."})


class TalentUpdateView(generics.UpdateAPIView):
    queryset = Talent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TalentUpdateSerializer

    def get_queryset(self):
        return Talent.objects.filter(pk=self.kwargs['pk'], tutor__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        talent = Talent.objects.get(pk=kwargs['pk'])

        if talent.title != request.data.get('title', ''):
            data = {
                'title': request.data.get('title', ''),
            }
            if verify_duplicate(Talent, data=data):
                return Response(data={"detail": "같은 제목의 수업이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_200_OK, data=success_update)


class TalentDeleteView(generics.DestroyAPIView):
    queryset = Talent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Talent.objects.filter(pk=self.kwargs['pk'], tutor__user=self.request.user)
