from rest_framework import generics

from talent.models import Talent, Curriculum, ClassImage, Location, WishList, Registration
from talent.serializers import CurriculumSerializer, ClassImageSerializer, TalentListSerializer, LocationSerializer, \
    WishListSerializer, RegistrationSerializer
from talent.serializers import LocationWrapperSerializers, TalentDetailSerializer, RegistrationWrapperSerializers
from talent.serializers import ReviewWrapperSerializer
from utils.pagination import TalentPagination

__all__ = (
    'TalentList',
    'CurriculumList',
    'ClassImageList',
    'LocationRetrieve',
    'WishList',
    'RegistrationList',
    # 'RegistrationRetrieve',
    'TalentRegistrationRetrieveView',
    'TalentDetail',
    'LocationList',
    'ReviewRetrieve',
)


# talent 전체 api
class TalentList(generics.ListAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializer
    pagination_class = TalentPagination


class LocationRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializers


class TalentRegistrationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = RegistrationWrapperSerializers
    #
    # def get_queryset(self):
    #     return Talent.objects.filter(pk=self.kwargs['pk'])
    # pagination_class = RegistrationPagination

    # def get(self, request, *args, **kwargs):
    #     registration = []
    #     locations = Location.objects.filter(talent=kwargs['pk'])
    #     print(locations)
    #     for location in locations:
    #         registration = location.registration_set.all()
    #     # page = self.paginate_queryset(registration)
    #     # if page is not None:
    #     #     serializer = self.get_serializer(page, many=True)
    #     #     return self.get_paginated_response(serializer.data)
    #
    #     serializer = RegistrationWrapperSerializers(registration, many=True)
    #     return Response(serializer.data)


# 하나의 talent에 대한 세부 정보 api
class TalentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentDetailSerializer


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

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


# class RegistrationRetrieve(generics.RetrieveAPIView):
#     queryset = Talent.objects.all()
#     serializer_class = RegistrationWrapperSerializers
#
#     def get_queryset(self):
#         return Talent.objects.filter(id=self.kwargs['pk'])


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class ReviewRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ReviewWrapperSerializer

    def get_queryset(self):
        return Talent.objects.filter(id=self.kwargs['pk'])
