from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import TalentPagination

__all__ = (
    'TalentList',
    'LocationList',
    'Curriculum',
    'ClassImage',
    'WishList',
    'RegistrationList',
    'TalentRegistration',
)

from talent.models import Talent, Curriculum, ClassImage, Location, WishList, Registration
from talent.serializers import CurriculumSerializers, ClassImageSerializers, TalentListSerializers, LocationSerializers, \
    WishListSerializers, RegistrationSerializer


class TalentList(generics.ListCreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializers
    pagination_class = TalentPagination


class TalentRegistration(APIView):
    def get(self, request, pk, *args, **kwargs):
        regis = Registration.objects.filter(talent_location=pk)
        print(regis)
        serializer = RegistrationSerializer(regis, many=True)
        return Response(serializer.data)


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


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
