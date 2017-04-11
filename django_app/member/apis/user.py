from django.contrib.auth import get_user_model
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
from talent.models import WishList, Talent
from talent.serializers import MyRegistrationWrapperSerializer
from talent.serializers.wish_list import MyWishListSerializer

__all__ = (
    'UserProfileView',
    'TutorProfileView',
    'UserRetrieveUpdateDestroyView',
    'CreateDjangoUserView',
    'MyWishListView',
    'MyRegistrationView',
    'WishListToggleView',
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
        print(request.data.keys())
        serializer = UserSerializer(user, data=request.data,
                                    partial=True)
        for request_item in request.data.keys():
            print(request_item)
            if request_item not in [item for item in UserSerializer(user).fields]:
                print(UserSerializer(user).fields)
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "잘못된 형식의 data 입니다"})
            elif serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED, data=UserSerializer(user).data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "잘못된 형식의 data 입니다"})

    # def patch(self, request, *args, **kwargs):
    #     user = request.user
    #     print(request.data)
    #     # 유저에 들어갈 필수 정보들이 있는지 체크. 없으면 에러 출력
    #     try:
    #         user.nickname = request.data['nickname']
    #     except MultiValueDictKeyError:
    #         ret = {
    #             'non_field_errors': [
    #                 '필수 항목을 채워주십시오.',
    #             ]
    #         }
    #         return Response(ret)
    #
    #     user.save()
    #     # 여기서 request.data로 넘겨받은 값을 수정
    #     # 수정된 값에 대해 validate
    #     # save()
    #     # return Response(serializer.data)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)


    def delete(self, request, format=None):
        user = request.user
        user.delete()
        ret = {
            "detail": "Successfully deleted"
        }
        return Response(ret)


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
                    return Response(status=status.HTTP_200_OK, data=MyWishListSerializer(user).data)
                else:
                    WishList.objects.create(user=user, talent=talent)
                    return Response(status=status.HTTP_201_CREATED, data=MyWishListSerializer(user).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': '본인의 수업을 위시리스트에 담을 수 없습니다.'})
        except Talent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': '해당 수업을 찾을 수 없습니다'})


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
