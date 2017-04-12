from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Tutor
from member.serializers import TutorSerializer
from member.serializers import UserSerializer
from member.serializers.login import CustomRegisterSerializer
from talent.models import WishList, Talent, Registration
from talent.serializers import MyRegistrationWrapperSerializer, TalentShortInfoSerializer
from talent.serializers.registration import TalentRegistrationSerializer
from talent.serializers.wish_list import MyWishListSerializer
from utils import verify_instance
from utils.remove_all_but_numbers import remove_non_numeric

__all__ = (
    'UserProfileView',
    'TutorProfileView',
    'UserRetrieveUpdateDestroyView',
    'CreateDjangoUserView',
    'MyWishListView',
    'MyRegistrationView',
    'WishListToggleView',
    'StaffUserVerifyTutorView',
    'StaffUserVerifyTalentView',
    'TutorVerifyRegistrationView',
)

User = get_user_model()


# ##### 일반 유저 관련 #####
class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            for request_item in request.data.keys():
                if request_item not in [item for item in UserSerializer(user).fields]:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "잘못된 형식의 data 입니다."})
            cellphone = request.data.get("cellphone", False)
            if cellphone and len(request.data["cellphone"]) == len(remove_non_numeric(cellphone)):
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
            elif cellphone and len(request.data["cellphone"]) != len(remove_non_numeric(cellphone)):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "cellphone 에는 숫자만 입력해주세요."})
            else:
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "잘못된 형식의 data 입니다."})
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "잘못된 형식의 data 입니다."})

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        ret = {
            "detail": "Successfully deleted"
        }
        return Response(ret)


class StaffUserVerifyTalentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, talent_pk):
        user = request.user
        try:
            if user.is_staff:
                talent, detail = verify_instance(Talent, talent_pk)
                return Response(status=status.HTTP_200_OK,
                                data={"detail": detail, "result": TalentShortInfoSerializer(talent).data})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "해당 요청에 대한 권한이 없습니다."})
        except Talent.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "해당 수업을 찾을 수 없습니다."})


class StaffUserVerifyTutorView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, tutor_pk):
        user = request.user
        try:
            if user.is_staff:
                tutor, detail = verify_instance(Tutor, tutor_pk)
                return Response(status=status.HTTP_200_OK,
                                data={"detail": detail, "result": TutorSerializer(tutor).data})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "해당 요청에 대한 권한이 없습니다."})
        except Tutor.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "해당 튜터를 찾을 수 없습니다."})


class TutorVerifyRegistrationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, registration_pk):
        user = request.user
        try:
            registration = Registration.objects.get(pk=registration_pk)
            if registration.talent_location.talent in user.talent_set.all():
                registration, detail = verify_instance(Registration, registration_pk)
                return Response(status=status.HTTP_200_OK,
                                data={"detail": detail, "result": TalentRegistrationSerializer(registration).data})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "해당 요청에 대한 권한이 없습니다."})
        except Registration.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "해당 신청 내역을 찾을 수 없습니다."})


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


# ##### 튜터 관련 #####
class TutorProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = TutorSerializer(Tutor.objects.get(user_id=user.id))
        return Response(serializer.data)


class CreateDjangoUserView(RegisterView):
    serializer_class = CustomRegisterSerializer


class MyWishListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = MyWishListSerializer(user)
        return Response(serializer.data)


# ##### 유저가 wishlist에 담기/빼기 #####
class WishListToggleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = User.objects.get(id=request.user.id)
        try:
            talent = Talent.objects.get(pk=pk)
            if talent.tutor.user != user:
                if talent.pk in user.my_wishlist.values_list('talent', flat=True):
                    wishlist = WishList.objects.filter(user=user, talent=talent)
                    wishlist.delete()
                    return Response(status=status.HTTP_200_OK, data={'detail': 'wishlist에서 삭제되었습니다.'})
                else:
                    WishList.objects.create(user=user, talent=talent)
                    return Response(status=status.HTTP_201_CREATED, data=MyWishListSerializer(user).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': '본인의 수업을 위시리스트에 담을 수 없습니다.'})
        except Talent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': '해당 수업을 찾을 수 없습니다.'})


class MyRegistrationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = MyRegistrationWrapperSerializer(user)
        return Response(serializer.data)

# class MyWishListRetrieve(generics.RetrieveAPIView):
#     serializer_class = MyWishListSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)
#
# class MyRegistrationRetrieve(generics.RetrieveAPIView):
#     serializer_class = MyRegistrationWrapperSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)
#
#     def empty_view(self):
#         content = {'error': '요청하신 유저의 정보와 pk가 불일치 합니다'}
#         return Response(content, status=status.HTTP_404_NOT_FOUND)
