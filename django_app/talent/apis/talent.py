from django.contrib.auth import get_user_model
from rest_framework import generics

from talent.serializers.registration import TalentRegistrationSerializer, TalentRegistrationWrapperSerializer
from talent.serializers import ReviewWrapperSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from talent.models import Talent, Curriculum, ClassImage, Registration
from talent.serializers import CurriculumSerializer, ClassImageSerializer, TalentListSerializer, LocationSerializer, \
    CurriculumWrapperSerializers, TalentShortDetailSerializer

from talent.serializers import LocationWrapperSerializers, TalentDetailSerializer
from talent.serializers.class_image import ClassImageWrapperSerializers
from utils.pagination import TalentPagination

__all__ = (
    # talent
    'TalentList',
    # detail - all
    'TalentDetail',
    # detail - fragments
    'TalentShortDetail',
    'CurriculumList',
    'ClassImageList',
    'LocationRetrieve',
    'ClassImageRetrieve',
    'CurriculumRetrieve',
    'ReviewRetrieve',

    # registration
    'TalentRegistrationRetrieve',

    # 'MyWishList',
    # 'MyRegistrationList',
    # 'RegistrationList',

    # 'LocationList',
)

User = get_user_model()


# talent 전체 api
class TalentList(generics.ListAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializer
    # pagination_class = TalentPagination
    lookup_field = 'pk'


class LocationRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializers


class TalentRegistrationRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentRegistrationWrapperSerializer
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


class ClassImageRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ClassImageWrapperSerializers


class CurriculumRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = CurriculumWrapperSerializers


class TalentShortDetail(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentShortDetailSerializer


# 하나의 talent에 대한 세부 정보 api
class TalentDetail(generics.RetrieveAPIView):
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


# class MyWishList(generics.ListAPIView):
#     serializer_class = MyWishListSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)
#
#
# class MyRegistrationList(generics.ListAPIView):
#     serializer_class = MyRegistrationListSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)


# class RegistrationRetrieve(generics.RetrieveAPIView):
#     queryset = Talent.objects.all()
#     serializer_class = RegistrationWrapperSerializers
#
#     def get_queryset(self):
#         return Talent.objects.filter(id=self.kwargs['pk'])


class ReviewRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ReviewWrapperSerializer


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationSerializer
