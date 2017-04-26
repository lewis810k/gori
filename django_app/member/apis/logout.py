from django.contrib.auth import (
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = (
    'CustomLogoutView',
)


class CustomLogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            # 커스터마이징 부분
            return Response({"detail": _("토큰이 제공되지 않았습니다.")},
                            status=status.HTTP_401_UNAUTHORIZED)

        django_logout(request)

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)
