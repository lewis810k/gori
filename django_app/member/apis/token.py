import requests
from django.contrib.auth import get_user_model
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = (
    'ObtainAuthToken',
)

User = get_user_model()


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if 'access_token' in request.data.keys():
            data = {
                'access_token': request.data['access_token'],
            }
            url = 'https://graph.facebook.com/me?fields=id,name'
            response = requests.get(url, params=data)
            response_json = response.json()
            # print(response.json())
            # {'name': 'Lewis Kim', 'id': '101541050xxxxx'}
            user = User.objects.get(username=response_json['id'])
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            print(type(user))
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()
