from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^profile/$', apis.UserProfileView.as_view()),
]
