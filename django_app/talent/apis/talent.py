from rest_framework import generics

from talent.models import Talent, Curriculum, ClassImage, Location
from talent.serializers import CurriculumSerializers, ClassImageSerializers, TalentListSerializers, LocationSerializers, \
    TalentDetailSerializers
from utils.pagination import TalentPagination

__all__ = (
    'TalentList',
    'TalentDetail',
    'LocationList',
    'CurriculumList',
    'ClassImageList',
)


# talent 전체 api
class TalentList(generics.ListAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializers
    pagination_class = TalentPagination


# 하나의 talent에 대한 세부 정보 api
class TalentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentDetailSerializers


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers


class CurriculumList(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializers


class ClassImageList(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializers
