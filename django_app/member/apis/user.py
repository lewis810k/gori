from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Tutor
from member.serializers import TutorSerializer
from member.serializers import UserSerializer, CustomLoginSerializer

User = get_user_model()

__all__ = (
    'UserProfileView',
    'TutorProfileView',
    'UserRetrieveUpdateDestroyView',
    'CreateDjangoUserView',
)

# ##### 일반 유저 관련 #####
class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        print(request.data)
        # 여기서 request.data로 넘겨받은 값을 수정
        # 수정된 값에 대해 validate
        # save()
        # return Response(serializer.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response('delete')


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
    serializer_class = CustomLoginSerializer
