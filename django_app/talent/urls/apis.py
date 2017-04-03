from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentDetail.as_view()),
    url(r'^list/location/$', apis.LocationList.as_view()),
]
