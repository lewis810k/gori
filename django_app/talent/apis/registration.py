from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Registration, Location
from talent.serializers import TalentRegistrationWrapperSerializer
from talent.serializers.registration import TalentRegistrationSerializer
from utils import tutor_verify

__all__ = (
    'TalentRegistrationRetrieveView',
    'RegistrationListCreateView',
)


class TalentRegistrationRetrieveView(generics.RetrieveAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentRegistrationWrapperSerializer


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        요청하는 장소에 대한 talent를 구한다. talent의 튜터가 request.user와 동일하면 에러.
        동일하지 않으면 등록 요청을 한다.

        필수정보 :
            - location_pk : 장소 아이디
            - message_to_tutor : 튜터에게 보내는 메시지
        추가정보 :
            - student_level : 학생 레벨
            - experience_length : 경력 (개월수)
        """
        try:
            location_pk = request.data['location_pk']
            location = Location.objects.filter(pk=location_pk).first()
            if not location:
                ret = {
                    'detail': 'location({pk})을 찾을 수 없습니다.'.format(pk=location_pk)
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            talent = location.talent

            # 해당 수업에 자신이 튜터라면 등록되지 않도록.
            if tutor_verify(request, talent):
                ret = {
                    'detail': '자신의 수업은 신청할 수 없습니다.',
                }
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 기존에 존재하는 아이템이면 생성되지 않도록
                item, created = Registration.objects.get_or_create(
                    student=request.user,
                    talent_location=location,
                    message_to_tutor=request.data['message_to_tutor'],

                    # 필수가 아닌 정보들
                    student_level=request.data.get('student_level', 1),
                    experience_length=request.data.get('experience_length', 0),
                )

                if not created:
                    ret = {
                        'detail': '이미 등록된 수업입니다.'
                    }
                    return Response(ret, status=status.HTTP_400_BAD_REQUEST)

                ret_message = '[{user}]님이 [{location}] 수업을 추가되었습니다.'.format(
                    user=request.user,
                    location=location
                )
                ret = {
                    'detail': ret_message,
                }
                return Response(ret, status=status.HTTP_201_CREATED)

        except MultiValueDictKeyError as e:
            ret = {
                'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
            }
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

# class RegistrationRetrieve(generics.RetrieveAPIView):
#     queryset = Talent.objects.all()
#     serializer_class = RegistrationWrapperSerializers
#
#     def get_queryset(self):
#         return Talent.objects.filter(id=self.kwargs['pk'])
