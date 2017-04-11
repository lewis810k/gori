from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import LocationWrapperSerializer, LocationCreateSerializer, LocationSerializer
from utils import tutor_verify, duplicate_verify

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
        try:
            talent_pk = request.data['talent_pk']
            region = request.data['region']
            specific_location = request.data['specific_location']
            day = request.data['day']
            time = request.data['time']
            extra_fee = request.data['extra_fee']
            talent = Talent.objects.get(pk=talent_pk)

            data = {
                'talent': talent,
                'region': region,
                'day': day
            }
            is_dup, msg = duplicate_verify(Location, data)
            if is_dup:
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

            if tutor_verify(request, talent):
                Location.objects.create(
                    talent=talent,
                    region=region,
                    specific_location=specific_location,
                    day=day,
                    time=time,
                    extra_fee=extra_fee,
                    # 필수정보가 아닌 경우 아래에 해당
                    extra_fee_amount=request.data.get('extra_fee_amount', ''),
                    location_info=request.data.get('location_info', ''),
                )

                ret_message = '[{talent}]에 [{region}] 지역이 추가되었습니다.'.format(
                    talent=talent.title,
                    region=region
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

            ret = {
                'detail': '권한이 없습니다.',
            }
            return Response(ret, status=status.HTTP_401_UNAUTHORIZED)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
