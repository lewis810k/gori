from rest_framework import generics

from talent.models import Talent
from talent.serializers import ReviewWrapperSerializer

__all__ = (
    'ReviewRetrieveView',
)


class ReviewRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ReviewWrapperSerializer
