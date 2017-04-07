from django.conf.urls import url

from .. import apis

app_name = 'talent'

urlpatterns = [
    # url(r'^list/location/$', apis.LocationList.as_view()),
    # url(r'^wishlist/$', apis.WishList.as_view()),
    url(r'^list/$', apis.TalentListView.as_view(), ),
    url(r'^detail-all/(?P<pk>[0-9]+)/$', apis.TalentDetailView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentShortDetailView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/location/$', apis.LocationRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/class-image/$', apis.ClassImageRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/curriculum/$', apis.CurriculumRetrieveView.as_view()),
    # url(r'^registration/$', apis.RegistrationList.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/registration/$', apis.TalentRegistrationRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/review/$', apis.ReviewRetrieveView.as_view()),
]
