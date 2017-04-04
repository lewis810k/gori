from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.helpers import complete_social_login
from rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError

__all__ = (
    'CustomLoginSerializer',
    'CustomSocialLoginSerializer',
)


class CustomLoginSerializer(RegisterSerializer):
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        user.name = request.POST['name']
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
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
