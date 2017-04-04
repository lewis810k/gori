from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import TalentPagination
from talent.serializers import LocationWrapperSerializers, TalentDetailSerializer
from talent.models import Talent, Curriculum, ClassImage, Location, WishList, Registration
from talent.serializers import CurriculumSerializer, ClassImageSerializer, TalentListSerializer, LocationSerializer, \
    WishListSerializer, RegistrationSerializer

__all__ = (
    'TalentList',
    'CurriculumList',
    'ClassImageList',
    'LocationRetrieve',
    'WishList',
    'RegistrationList',
    'TalentRegistration',
    'TalentDetail',
    # 'LocationList',
)


# talent 전체 api
class TalentList(generics.ListAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializer
    pagination_class = TalentPagination


class LocationRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializers

    def get_queryset(self):
        return Talent.objects.filter(id=self.kwargs['pk'])


class TalentRegistration(APIView):
    def get(self, request, pk, *args, **kwargs):
        regis = Registration.objects.filter(talent_location=pk)
        print(regis)
        serializer = RegistrationSerializer(regis, many=True)
        return Response(serializer.data)


# 하나의 talent에 대한 세부 정보 api
class TalentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentDetailSerializer


# class LocationList(generics.ListAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.save(
    #         photo_set=request.data.getlist('photo')
    #     )
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurriculumList(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer


class ClassImageList(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializer


class WishList(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
