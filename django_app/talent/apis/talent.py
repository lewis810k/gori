from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions

from talent.models import Talent
from talent.serializers import TalentDetailSerializer
from talent.serializers import TalentListSerializer, TalentShortDetailSerializer

__all__ = (
    'TalentListCreateView',
    # detail - all
    'TalentDetailView',
    # detail - fragments
    'TalentShortDetailView',
)

User = get_user_model()


# talent 전체 api
class TalentListCreateView(generics.ListCreateAPIView):
    serializer_class = TalentListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # pagination_class = TalentPagination

    # rest_framework의 SearchFilter 사용시
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('title', 'class_info')

    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user.tutor)

    def get_queryset(self):
        queryset = Talent.objects.all()
        title = self.request.query_params.get('title', None)
        region = self.request.query_params.get('region', None)
        category = self.request.query_params.get('category', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if region is not None:
            queryset = queryset.filter(locations__region__icontains=region).distinct('pk')
        if category is not None:
            queryset = queryset.filter(category__icontains=category)

        return queryset


class TalentShortDetailView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentShortDetailSerializer


# 하나의 talent에 대한 세부 정보 api
class TalentDetailView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentDetailSerializer
