from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Curriculum, Talent
from talent.serializers import CurriculumSerializer, CurriculumWrapperSerializer
from utils import tutor_verify, LargeResultsSetPagination

__all__ = (
    'CurriculumListCreateView',
)


class CurriculumListCreateView(generics.ListCreateAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Curriculum.objects.filter(talent_id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """

        필수정보 :
            - talent_pk : 수업 아이디
            - information : 커리큘럼 설명
        추가정보 :
            - image : 커리큘럼 이미지
        """
        try:
            talent_pk = request.data['talent_pk']
            talent = Talent.objects.filter(pk=talent_pk).first()
            if not talent:
                ret = {
                    'detail': '수업({pk})이 존재하지 않습니다.'.format(pk=talent_pk)
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            if tutor_verify(request, talent):
                item, _ = Curriculum.objects.get_or_create(
                    talent=talent,
                    information=request.data['information'],
                    image=request.FILES.get('image', ''),
                )
                ret_message = '[{talent}]에 수업이 추가되었습니다.'.format(
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

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)


class CurriculumRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = CurriculumWrapperSerializer
