from rest_framework import generics

from talent.models import Talent
from talent.serializers import LocationWrapperSerializers

__all__ = (
    'LocationRetrieveView',
)


class LocationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializers


# class LocationList(generics.ListAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
