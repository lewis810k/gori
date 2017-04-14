from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Review
from talent.serializers import ReviewWrapperSerializer, ReviewSerializer
from utils import tutor_verify, LargeResultsSetPagination

__all__ = (
    'ReviewRetrieveView',
    'ReviewCreateView',
    'ReviewListView',
)


#
class ReviewRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = ReviewWrapperSerializer


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Review.objects.filter(talent_id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

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

            talent = Talent.objects.filter(pk=talent_pk).first()
            if not talent:
                ret = {
                    'detail': '수업({pk})이 존재하지 않습니다.'.format(pk=talent_pk)
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

            # 자신의 수업이 아니어야 등록 가능
            if not tutor_verify(request, talent):
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
                # 이미 리뷰가 존재하면 등록할 수 없음
                if not created:
                    ret = {
                        'detail': '리뷰는 1개만 등록할 수 있습니다.'
                    }
                    return Response(ret, status=status.HTTP_400_BAD_REQUEST)

                ret_message = '[{talent}]에 리뷰가 추가되었습니다.'.format(
                    talent=talent.title,
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

            # 자신의 수업에 리뷰를 등록하려는 경우
            else:
                ret = {
                    'detail': '자신의 수업에 리뷰를 등록할 수 없습니다.',
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
