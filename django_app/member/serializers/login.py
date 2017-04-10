from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.helpers import complete_social_login

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError
from rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from rest_framework import serializers

__all__ = (
    'CustomLoginSerializer',
    'CustomSocialLoginSerializer',
)

User = get_user_model()


class CustomLoginSerializer(RegisterSerializer):
    name = serializers.CharField(write_only=True)
    #
    # def validate_name(self, name):
    #     name = get_adapter().clean_username(name)
    #     return name

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        print('1')
        adapter = get_adapter()
        print('2')
        user = adapter.new_user(request)
        print(user)
        if 'name' in request.POST:
            user.name = request.POST['name']
        print(user.name)
            # else:
            #     raise Exception('test')
            #     # return HttpResponse('test')
            # raise MultiValueDictKeyError('test')
        #
        # try:
        #     user.name = request.POST['name']
        # except MultiValueDictKeyError as ME:
        #     print(ME)
        # finally:
        #     raise ValueError('could not find {} in {}'.format(char, char_string))
        print('3')
        self.cleaned_data = self.get_cleaned_data()
        print(self.cleaned_data)
        print('4')
        print(request, user)
        adapter.save_user(request, user, self)
        print('5')
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        print('6')
        return user


class CustomSocialLoginSerializer(SocialLoginSerializer):
    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()
        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        if attrs.get('access_token'):
            access_token = attrs.get('access_token')
        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user
        return attrs
