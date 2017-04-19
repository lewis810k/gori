from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import LocationSerializer, LocationCreateSerializer
from utils import *

__all__ = (
    'LocationListCreateView',
    'LocationDeleteView',
    'LocationUpdateView'
)


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Location.objects.filter(talent_id=self.kwargs['pk'])

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
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)

class LocationUpdateView(generics.UpdateAPIView):
    queryset = Location.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LocationCreateSerializer

    def get_queryset(self):
        return Location.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        location = Location.objects.get(pk=kwargs['pk'])
        talent = location.talent
        if location.region == request.data['region'] and location.day == request.data['day']:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        else:
            data = {
                'talent': talent,
                'region': request.data['region'],
                'day': request.data['day'],
            }
            if verify_duplicate(Location, data=data):
                return Response(data={"detail":"지역 중복 or 요일 중복"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_200_OK, data=success_update)

class LocationDeleteView(generics.DestroyAPIView):
    queryset = Location.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Location.objects.filter(pk=self.kwargs['pk'], talent__tutor__user=self.request.user)
