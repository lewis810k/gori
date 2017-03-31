from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import TalentSerializers, LocationSerializers
from utils.pagination import TalentPagination

__all__ = (
    'TalentList',
    'LocationList',
)


class TalentList(generics.ListCreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentSerializers
    pagination_class = TalentPagination


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.save(
    #         photo_set=request.data.getlist('photo')
    #     )
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
