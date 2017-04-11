from rest_framework import generics

from talent.models import Talent
from talent.serializers import QnAWrapperSerializer

__all__ = (
    'QnATalentRetrieveView',
)


class QnATalentRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = QnAWrapperSerializer
