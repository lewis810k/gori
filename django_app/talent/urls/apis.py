from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),
    url(r'^wishlist/$', apis.WishList.as_view()),
    url(r'^list/location/$', apis.LocationList.as_view()),
    url(r'^registration/$', apis.RegistrationList.as_view()),
    url(r'^(?P<pk>[0-9]+)/registration/$', apis.TalentRegistration.as_view()),
]
