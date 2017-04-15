from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, ClassImage
from talent.serializers import ClassImageWrapperSerializer, ClassImageSerializer
from utils import verify_tutor, LargeResultsSetPagination

__all__ = (
    'ClassImageListCreateView',
)


class ClassImageListCreateView(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return ClassImage.objects.filter(talent_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """

        필수정보 :
            - talent_pk : 수업 아이디
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

            if verify_tutor(request, talent):
                ClassImage.objects.create(
                    talent=talent,
                    image=request.FILES['image'],
                )
                ret_message = '[{talent}]에 [{image}]가 추가되었습니다.'.format(
                    talent=talent.title,
                    image=request.FILES['image'],
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