from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^profile/$', apis.ProfileView.as_view()),

]
