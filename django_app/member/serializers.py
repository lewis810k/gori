from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.helpers import complete_social_login
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from member.models import Tutor
from requests.exceptions import HTTPError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'name',
            'user_type',
            'is_staff',
            'is_active',
            'cellphone',
            'profile_image',
            'joined_date',
            'is_tutor',
            'last_login',
        )

    def get_user_type(self, obj):
        return obj.get_user_type_display()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TutorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        read_only=True, source='user.username')
    name = serializers.CharField(
        read_only=True, source='user.name'
    )
    cellphone = serializers.CharField(
        read_only=True, source='user.cellphone'
    )
    profile_image = serializers.ImageField(
        read_only=True, source='user.profile_image')

    class Meta:
        model = Tutor
        fields = (
            'pk',
            'username',
            'name',
            'user',
            'is_verified',
            'profile_image',
            'cellphone',
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
        """
        :param adapter: allauth.socialaccount Adapter subclass.
            Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the
            `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        # print('response: ', response)
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        print(self.context.get('request').data)
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

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        # Case 1: We received the access_token
        if attrs.get('access_token'):
            access_token = attrs.get('access_token')
        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            # print(login)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            login.lookup()
            # print(login)
            login.save(request, connect=True)
        attrs['user'] = login.account.user
        # print(dir(login.account.user))
        # print(dir(login.lookup.__str__()))
        # print(attrs)
        return attrs
