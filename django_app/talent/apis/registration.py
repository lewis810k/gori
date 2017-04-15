from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from talent.models import Talent, Registration, Location
from talent.serializers import TalentRegistrationWrapperSerializer
from talent.serializers.registration import TalentRegistrationSerializer, TalentRegistrationCreateSerializer
from utils import *

__all__ = (
    'RegistrationListCreateView',
)


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Registration.objects.filter(talent_location__talent_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
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
        request.data['user'] = request.user.id

        # 생성 전용 시리얼라이저 사용
        serializer = TalentRegistrationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ##### 추가 검증 절차 #####
        location = Location.objects.get(pk=request.data['location_pk'])
        talent = location.talent

        # ##### 자신의 수업이면 등록 불가능 #####
        if verify_tutor(request, talent):
            return Response(talent_owner_error, status=status.HTTP_400_BAD_REQUEST)

        # ##### 이미 등록되었는지 #####
        data = {
            'student': request.user,
            'talent_location': location,
        }
        if verify_duplicate(Registration, data=data):
            return Response(multiple_item_error, status=status.HTTP_400_BAD_REQUEST)
        # ##### 추가 검증 끝 #####

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)

    # def post(self, request, *args, **kwargs):
    #
    #     try:
    #         request.data['talent_location'] = request.data['location_pk']
    #         request.data['student'] = request.user.id
    #     except MultiValueDictKeyError as e:
    #         ret = {
    #             'non_field_error': (str(e)).strip('"') + ' field가 제공되지 않았습니다.'
    #         }
    #         return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    #     return self.create(request, *args, **kwargs)