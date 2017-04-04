import requests
from allauth.account.adapter import get_adapter
from allauth.socialaccount.providers.facebook.provider import FacebookProvider, GRAPH_API_URL
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter, compute_appsecret_proof
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import RegisterView, SocialLoginView
from rest_auth.views import LoginView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount import app_settings, providers

from member.serializers import UserSerializer, CustomLoginSerializer, CustomSocialLoginSerializer

User = get_user_model()

__all__ = (
    'UserProfileView',
    'TutorProfileView',
    'DestroyUserView',
    'CreateDjangoUserView',
    'CreateFacebookUserView',
)


class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class TutorProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class DestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class CreateDjangoUserView(RegisterView):
    serializer_class = CustomLoginSerializer


def fb_complete_login(request, app, token):
    provider = providers.registry.by_id(FacebookProvider.id, request)
    resp = requests.get(
        GRAPH_API_URL + '/me',
        params={
            'fields': ','.join(provider.get_fields()),
            'access_token': token.token,
            'appsecret_proof': compute_appsecret_proof(app, token)
        })

    resp.raise_for_status()

    extra_data = resp.json()
    print(extra_data)
    print('===========')
    extra_data['username'] = extra_data['id']
    # request.data['user_type'] = 'f'
    login = provider.sociallogin_from_response(request, extra_data)
    print(login.user)
    login.user.name = extra_data['name']
    login.user.user_type = 'f'
    # 이거는.. 모든 생성 과정 끝나면 이미지 따로 업로드 하는 것으로!!!!
    # login.user.profile_image = 'https://graph.facebook.com/' + login.user.username + '/picture'
    print('---------------')
    print(dir(login.user))
    return login


class FacebookOAuth2TempAdapter(OAuth2Adapter):
    provider_id = FacebookProvider.id
    provider_default_auth_url = 'https://www.facebook.com/dialog/oauth'

    settings = app_settings.PROVIDERS.get(provider_id, {})

    authorize_url = settings.get('AUTHORIZE_URL', provider_default_auth_url)
    access_token_url = GRAPH_API_URL + '/oauth/access_token'
    expires_in_key = 'expires_in'

    def complete_login(self, request, app, access_token, **kwargs):
        return fb_complete_login(request, app, access_token)


class CreateFacebookUserView(SocialLoginView):
    adapter_class = FacebookOAuth2TempAdapter
    serializer_class = CustomSocialLoginSerializer
