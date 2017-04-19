from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from talent.serializers import RegistrationUpdateSerializer
from talent.serializers.registration import TalentRegistrationSerializer, TalentRegistrationCreateSerializer
from utils import *

__all__ = (
    'RegistrationListCreateView',
    'RegistrationDeleteView',
    'RegistrationUpdateView',
)


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = TalentRegistrationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Registration.objects.filter(talent_location__talent_id=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        """
        pk에 해당하는 talent의 작성자가 request.user인지 확인하고 정보 출력
        """
        user = request.user

        # talent pk가 존재하는지, 없으면 다른 리스트 반환값 처럼 반환. 여기만 예외적으로!!
        try:
            talent = Talent.objects.get(pk=kwargs['pk'])
        except Talent.DoesNotExist as de:
            return Response(object_not_found, status=status.HTTP_200_OK)

        # 요청하는 유저가 튜터인지
        try:
            tutor = user.tutor
        except ObjectDoesNotExist as e:
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        # talent의 튜터와 요청하는 유저가 같은지
        if talent.tutor != tutor:
            return Response(authorization_error, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class RegistrationUpdateView(generics.UpdateAPIView):
    queryset = Registration.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegistrationUpdateSerializer

    def get_queryset(self):
        return Registration.objects.filter(pk=self.kwargs['pk'], student=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_200_OK, data=success_update)


class RegistrationDeleteView(generics.DestroyAPIView):
    queryset = Registration.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Registration.objects.filter(pk=self.kwargs['pk'], student=self.request.user)
