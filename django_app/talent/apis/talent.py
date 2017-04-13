from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent
from talent.serializers import TalentDetailSerializer
from talent.serializers import TalentListSerializer, TalentShortDetailSerializer
from utils import duplicate_verify, Tutor

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

    def post(self, request, *args, **kwargs):
        """

        필수정보 :
            - title : 수업 제목
            - category : 카테고리
            - type : 수업 형태
            - cover_image : 수업 이미지
            - tutor_info : 튜터 자기소개
            - class_info : 수업 소개
            - number_of_class : 한달기준 수업횟수
            - price_per_hour : 시간당 금액
            - hours_per_class : 회당 수업시간
        추가정보 :
            - video1 : 비디오링크 1
            - video2 : 비디오링크 2
        """
        try:
            title = request.data['title']
            category = request.data['category']
            type = request.data['type']
            cover_image = request.FILES['cover_image']
            tutor_info = request.data['tutor_info']
            class_info = request.data['class_info']
            number_of_class = request.data['number_of_class']
            price_per_hour = request.data['price_per_hour']
            hours_per_class = request.data['hours_per_class']
            video1 = request.data.get('video1', '')
            video2 = request.data.get('video2', '')

            user = request.user

            tutor_list = Tutor.objects.values_list('user_id', flat=True)

            # 요청하는 유저가 튜터인지 체크
            if user.id in tutor_list:
                # 이미 같은 이름의 수업이 존재하면 400 리턴
                data = {
                    'title': title,
                }
                is_dup, msg = duplicate_verify(Talent, data)
                if is_dup:
                    return Response(msg, status=status.HTTP_400_BAD_REQUEST)

                Talent.objects.create(
                    tutor=user.tutor,
                    title=title,
                    category=category,
                    type=type,
                    tutor_info=tutor_info,
                    class_info=class_info,
                    number_of_class=number_of_class,
                    price_per_hour=price_per_hour,
                    hours_per_class=hours_per_class,
                    cover_image=cover_image,
                    video1=video1,
                    video2=video2,
                )

                ret_message = '[{talent}] 수업이 추가되었습니다.'.format(
                    talent=title,
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

            ret = {
                'detail': '권한이 없습니다.',
            }
            return Response(ret, status=status.HTTP_401_UNAUTHORIZED)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

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
