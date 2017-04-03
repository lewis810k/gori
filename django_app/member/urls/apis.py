from django.conf.urls import url
from .. import apis
from rest_framework.authtoken import views as authtoken_views

urlpatterns = [
    url(r'^profile/user/$', apis.UserProfileView.as_view()),
    url(r'^profile/tutor/(?P<pk>[0-9]+)/$', apis.TutorProfileView.as_view()),
    url(r'^delete/(?P<pk>[0-9]+)/$', apis.DestroyUserView.as_view(), name='user-delete'),
    url(r'^token-auth/', authtoken_views.obtain_auth_token),
    url(r'^registration/', apis.CreateDjangoUserView.as_view()),
    url(r'^fb_registration/', apis.CreateFacebookUserView.as_view())
]
