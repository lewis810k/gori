from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import LocationSerializer, LocationCreateSerializer
from utils import *

__all__ = (
    'LocationListCreateView',
    'LocationDeleteView',
)


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering = ('-pk',)

    def get_queryset(self):
        return Location.objects.filter(talent_id=self.kwargs['pk'])

    # 여러개를 한번에 추가하려고 하는 경우. 초기 생성시에는 중복이 없다는 것을 가정!
    def create_list(self, request):
        for data in request.data['input_list']:
            # 생성 전용 시리얼라이저 사용
            serializer = LocationCreateSerializer(data=data)
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
            - region : 지역에 대한 키 값
            - specific_location : 세부 지역에 대한 결정 여부
            - day : 요일
            - time : 시간
            - extra_fee : 추가 요금 있는지 여부
        추가정보 :
            - extra_fee_amount : 추가 요금 설명
            - location_info : 장소 세부 정보
        """
        request.data['user'] = request.user.id

        if 'input_list' in request.data:
            self.create_list(request)
        else:

            # 생성 전용 시리얼라이저 사용
            serializer = LocationCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # ##### 추가 검증 절차 #####
            talent = Talent.objects.get(pk=request.data['talent_pk'])

            # ##### 자신의 수업이 아니면 등록 불가능 #####
            if not verify_tutor(request, talent):
                return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

            # ##### 같은 장소-요일이 존재하면 등록 불가능#####
            data = {
                'talent': talent,
                'region': request.data['region'],
                'day': request.data['day'],
            }
            if verify_duplicate(Location, data=data):
                return Response(multiple_item_error, status=status.HTTP_400_BAD_REQUEST)

            # ##### 추가 검증 끝  #####
            self.perform_create(serializer)

        return Response(success_msg, status=status.HTTP_201_CREATED)


class LocationDeleteView(generics.DestroyAPIView):
    queryset = Location.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Location.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)
