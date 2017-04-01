from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),
    url(r'^list/location/(?P<pk>[0-9]+)/$', apis.LocationRetrieve.as_view()),
]
