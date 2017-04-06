from django.conf.urls import url

from .. import apis

app_name = 'talent'

urlpatterns = [
    # url(r'^list/location/$', apis.LocationList.as_view()),
    # url(r'^wishlist/$', apis.WishList.as_view()),
    url(r'^list/$', apis.TalentList.as_view(), ),
    url(r'^detail-all/(?P<pk>[0-9]+)/$', apis.TalentDetail.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentShortDetail.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/location/$', apis.LocationRetrieve.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/class-image/$', apis.ClassImageRetrieve.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/curriculum/$', apis.CurriculumRetrieve.as_view()),
    # url(r'^registration/$', apis.RegistrationList.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/registration/$', apis.TalentRegistrationRetrieve.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/review/$', apis.ReviewRetrieve.as_view()),
]
