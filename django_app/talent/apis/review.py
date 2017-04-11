from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Review
from talent.serializers import ReviewWrapperSerializer, ReviewSerializer
from utils import tutor_verify

__all__ = (
    'ReviewRetrieveView',
    'ReviewCreateView',
)


class ReviewRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ReviewWrapperSerializer


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        """
        특정 수업에 대해 리뷰를 작성한다.
        자신의 수업에 대해서는 리뷰를 작성할 수 없도록 한다.

        필수정보 :
            - talent_pk : 수업 아이디
            - curriculum : 커리큘럼에 대한 점수
            - readiness : 준비성에 대한 점수
            - timeliness : 시간을 잘 지켰는지에 대한 점수
            - delivery : 전달력에 대한 점수
            - friendliness : 친근감?에 대한 점수
        추가정보 :
            - comment : 코멘트
        """
        try:

            talent_pk = request.data['talent_pk']
            user = request.user

            curriculum = request.data['curriculum']
            readiness = request.data['readiness']
            timeliness = request.data['timeliness']
            delivery = request.data['delivery']
            friendliness = request.data['friendliness']

            talent = Talent.objects.get(pk=talent_pk)
            # 자신이
            if not tutor_verify(request, talent):
                # 음.. 여긴 talent만 가리키고 있기 때문에.. 항상 추가만 되는군
                item, created = Review.objects.get_or_create(
                    talent=talent,
                    user=user,
                    curriculum=curriculum,
                    readiness=readiness,
                    timeliness=timeliness,
                    delivery=delivery,
                    friendliness=friendliness,
                    comment=request.data.get('comment', ''),
                )
                if not created:
                    ret = {
                        'detail': '리뷰는 1개만 등록할 수 있습니다.'
                    }
                    return Response(ret, status=status.HTTP_400_BAD_REQUEST)

                ret_message = '[{talent}]에 review가 추가되었습니다.'.format(
                    talent=talent.title,
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)
            else:
                ret = {
                    'detail': '자신의 수업에 평점을 리뷰를 등록할 수 없습니다.',
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
