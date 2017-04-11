from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import LocationWrapperSerializer, LocationCreateSerializer, LocationSerializer
from utils import tutor_verify

__all__ = (
    'LocationRetrieveView',
    'LocationCreateView',
)


class LocationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializer


class LocationCreateView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationCreateSerializer

    def post(self, request, *args, **kwargs):
        talent = Talent.objects.get(pk=request.data['talent_pk'])
        if tutor_verify(request, talent):
            try:
                Location.objects.create(
                    talent=talent,
                    region=request.data['region'],
                    specific_location=request.data['specific_location'],
                    day=request.data['day'],
                    time=request.data['time'],
                    extra_fee=request.data.get('extra_fee', 'N'),
                    extra_fee_amount=request.data.get('extra_fee_amount', ''),
                    location_info=request.data.get('location_info', ''),
                )
            except MultiValueDictKeyError as e:
                ret = {
                    'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            ret_message = '[{talent}]에 [{region}] 지역이 추가되었습니다.'.format(
                talent=talent.title,
                region=request.data['region']
            )
            ret = {
                'detail': ret_message,
            }
            return Response(ret, status=status.HTTP_201_CREATED)

        ret = {
            'detail': '권한이 없습니다.',
        }
        return Response(ret, status=status.HTTP_401_UNAUTHORIZED)
