from rest_framework import generics
from rest_framework.response import Response

from utils.pagination import TalentPagination
from talent.models import Talent, Curriculum, ClassImage, Location
from talent.serializers import CurriculumSerializers, ClassImageSerializers, TalentListSerializers, LocationSerializers, \
    LocationWrapperSerializers

__all__ = (
    'TalentList',
    'Curriculum',
    'ClassImage',
    'LocationRetrieve',
)


class TalentList(generics.ListCreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentListSerializers
    pagination_class = TalentPagination


class LocationRetrieve(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = LocationWrapperSerializers

    def get_queryset(self):
        return Talent.objects.filter(id=self.kwargs['pk'])



        #     return Response(serializer.data)

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
