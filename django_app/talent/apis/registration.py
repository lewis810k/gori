from rest_framework import generics

from talent.models import Talent
from talent.serializers import TalentRegistrationWrapperSerializer

__all__ = (
    'TalentRegistrationRetrieveView',
)


class TalentRegistrationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentRegistrationWrapperSerializer
