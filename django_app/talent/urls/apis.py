from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),
    url(r'^detail/location/(?P<pk>[0-9]+)/$', apis.LocationRetrieve.as_view()),
    url(r'^detail/classimage/(?P<pk>[0-9]+)/$', apis.ClassImageRetrieve.as_view()),
    url(r'^detail/curriculum/(?P<pk>[0-9]+)/$', apis.CurriculumRetrieve.as_view()),
    url(r'^mywishlist/$', apis.MyWishList.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentShortDetail.as_view()),
    url(r'^detail-all/(?P<pk>[0-9]+)/$', apis.TalentDetail.as_view()),
    url(r'^list/location/$', apis.LocationList.as_view()),
    url(r'^registration/$', apis.RegistrationList.as_view()),
    url(r'^(?P<pk>[0-9]+)/registration/$', apis.TalentRegistration.as_view()),
]
