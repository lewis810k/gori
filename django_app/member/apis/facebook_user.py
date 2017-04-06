from urllib.request import urlopen

import requests
from allauth.socialaccount.providers.facebook.provider import FacebookProvider, GRAPH_API_URL
from allauth.socialaccount.providers.facebook.views import compute_appsecret_proof, FacebookOAuth2Adapter
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount import providers

from member.serializers import CustomSocialLoginSerializer

User = get_user_model()

__all__ = (
    'CreateFacebookUserView',
)


def fb_profile_image_save(login):
    """
    페이스북 유저정보에서 유저id를 받아온다.
    유저id를 이용하여 프로필 사진을 불러온다.
        프로필 사진을 불러올 때 사이즈를 크게 한다.
    유저 정보에 이미지를 저장 한다.
    :return: login
    """
    image_url = 'https://graph.facebook.com/' + login.user.username + '/picture?type=large&width=200&height=200'
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()
    try:
        login.user.profile_image.save('image_{}.{}'.format(login.user.username, 'jpg'), File(img_temp))
    except IntegrityError as IE:
        print(IE)
    return login


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

    # 커스터마이징 시작
    # user 모델의 username 필드를 unique하게 저장하기 때문에 id값으로 변경한다.
    extra_data['username'] = extra_data['id']

    login = provider.sociallogin_from_response(request, extra_data)

    # soiciallogin을 통해서 채워진 데이터 이외에 추가정보를 입력한다.
    # name은 기존에 name을 이용하여 처리.
    login.user.name = extra_data['name']

    # facebook유저는 f로 구분
    login.user.user_type = 'f'

    # 프로필 이미지 받아오기
    login = fb_profile_image_save(login)
    return login


class FacebookOAuth2TempAdapter(FacebookOAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return fb_complete_login(request, app, access_token)


class CreateFacebookUserView(SocialLoginView):
    adapter_class = FacebookOAuth2TempAdapter
    serializer_class = CustomSocialLoginSerializer
