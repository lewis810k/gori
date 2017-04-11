from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Curriculum, Talent
from talent.serializers import CurriculumSerializer, CurriculumWrapperSerializer
from utils import tutor_verify

__all__ = (
    'CurriculumListCreateView',
    'CurriculumRetrieveView',
)


class CurriculumListCreateView(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

    def post(self, request, *args, **kwargs):
        talent = Talent.objects.get(pk=request.data['talent_pk'])
        if tutor_verify(request, talent):
            try:
                Curriculum.objects.create(
                    talent=talent,
                    information=request.data['information'],
                    image=request.FILES['image']
                )
            except MultiValueDictKeyError as e:
                ret = {
                    'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            ret_message = '[{talent}]에 [{information}] 수업이 추가되었습니다.'.format(
                talent=talent.title,
                information=request.data['information']
            )
            ret = {
                'detail': ret_message,
            }
            return Response(ret, status=status.HTTP_201_CREATED)

        ret = {
            'detail': '권한이 없습니다.',
        }
        return Response(ret, status=status.HTTP_401_UNAUTHORIZED)


class CurriculumRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = CurriculumWrapperSerializer
