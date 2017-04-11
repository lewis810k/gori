from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Location
from talent.serializers import LocationWrapperSerializer, LocationCreateSerializer, LocationSerializer

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

    # def create(self, request, *args, **kwargs):
    #     print(1)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer, **kwargs):
    #     print(2)
    #     serializer.save(talent=Talent.objects.get(pk=self.request.data['talent']))

