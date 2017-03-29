from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^profile/user/$', apis.UserProfileView.as_view()),
    url(r'^profile/tutor/(?P<pk>[0-9]+)/$', apis.TutorProfileView.as_view()),
]
