from django.conf.urls import url, include
from .. import apis
from rest_framework.authtoken import views as authtoken_views

urlpatterns = [
    url(r'^profile/user/$', apis.UserProfileView.as_view()),
    url(r'^profile/tutor/(?P<pk>[0-9]+)/$', apis.TutorProfileView.as_view()),
    url(r'^delete/(?P<pk>[0-9]+)/$', apis.DestroyUserView.as_view(), name='user-delete'),
    url(r'^token-auth/', apis.ObtainAuthToken.as_view()),
    url(r'^signup/', apis.CreateDjangoUserView.as_view()),
    url(r'^fb_login/', apis.CreateFacebookUserView.as_view()),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^', include('rest_auth.urls')),
]
