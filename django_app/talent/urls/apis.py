from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),
    url(r'^wishlist/$', apis.WishList.as_view()),
    url(r'^list/location/$', apis.LocationList.as_view()),
]
