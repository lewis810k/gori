from rest_framework import generics

from talent.models import Curriculum, Talent
from talent.serializers import CurriculumSerializer, CurriculumWrapperSerializer

__all__ = (
    'CurriculumListCreateView',
    'CurriculumRetrieveView',
)


class CurriculumListCreateView(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer


class CurriculumRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = CurriculumWrapperSerializer
