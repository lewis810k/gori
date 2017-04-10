from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from member.models import Tutor
from talent.models import Talent, ClassImage
from talent.serializers import ClassImageWrapperSerializers, ClassImageSerializer

__all__ = (
    'ClassImageListCreateView',
    'ClassImageRetrieveView',
)


class ClassImageListCreateView(generics.ListCreateAPIView):
    queryset = ClassImage.objects.all()
    serializer_class = ClassImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        talent = Talent.objects.get(pk=kwargs['pk'])
        tutor_list = Tutor.objects.values_list('user_id', flat=True)
        # 요청하는 유저가 튜터인지 확인
        if request.user.id in tutor_list:
            # 추가하고자 하는 talent의 튜터와 요청하는 유저(튜터)의 정보가 같은지 확인, 같으면 진행
            if talent.tutor == request.user.tutor:
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


class ClassImageRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ClassImageWrapperSerializers
