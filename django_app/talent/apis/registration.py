from rest_framework import generics

from talent.models import Talent, Registration
from talent.serializers import TalentRegistrationWrapperSerializer
from talent.serializers.registration import TalentRegistrationSerializer, TalentRegistrationCreateSerializer

__all__ = (
    'TalentRegistrationRetrieveView',
    'RegistrationListView',
    'RegistrationCreateView',
)


class TalentRegistrationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentRegistrationWrapperSerializer


class RegistrationListView(generics.ListAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationSerializer


class RegistrationCreateView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationCreateSerializer

# class RegistrationRetrieve(generics.RetrieveAPIView):
#     queryset = Talent.objects.all()
#     serializer_class = RegistrationWrapperSerializers
#
#     def get_queryset(self):
#         return Talent.objects.filter(id=self.kwargs['pk'])
