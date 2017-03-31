from django.views.generic import DetailView
from requests import Response
from rest_framework import generics
from rest_framework import status

from utils.pagination import TalentPagination

__all__ = (
    'TalentList',
    'LocationList',
    'Curriculum',
    'ClassImage',
    'WishList',
)

from talent.models import Talent, Curriculum, ClassImage, Location, WishList
from talent.serializers import CurriculumSerializers, ClassImageSerializers, TalentListSerializers, LocationSerializers, \
    WishListSerializers


class TalentList(generics.ListCreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializers
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


class Curriculum(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializers


class ClassImage(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializers


class WishList(generics.ListCreateAPIView):

    queryset = WishList.objects.all()
    serializer_class = WishListSerializers










