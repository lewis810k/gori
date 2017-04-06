from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

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
            return Response({"detail": _("토큰이 유효하지 않습니다.")},
                            status=status.HTTP_401_UNAUTHORIZED)

        logout(request)

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)
