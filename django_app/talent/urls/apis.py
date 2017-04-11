from django.conf.urls import url

from .. import apis

app_name = 'talent'

urlpatterns = [
    # url(r'^list/location/$', apis.LocationList.as_view()),
    # url(r'^wishlist/$', apis.WishList.as_view()),

    # ##### 생성 #####
    url(r'^create/$', apis.TalentListCreateView.as_view()),
    url(r'^add/class-image/$', apis.ClassImageListCreateView.as_view()),
    url(r'^add/location/$', apis.LocationCreateView.as_view()),
    url(r'^add/curriculum/$', apis.CurriculumListCreateView.as_view()),
    url(r'^add/registration/$', apis.RegistrationCreateView.as_view()),

    # ##### 리스트 #####
    url(r'^list/$', apis.TalentListCreateView.as_view()),

    # ##### 전체보기 #####
    url(r'^detail-all/(?P<pk>[0-9]+)/$', apis.TalentDetailView.as_view()),

    # ##### 요약 #####
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentShortDetailView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/location/$', apis.LocationRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/class-image/$', apis.ClassImageRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/curriculum/$', apis.CurriculumRetrieveView.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/registration/$', apis.TalentRegistrationRetrieveView.as_view()),
    # url(r'^registration/$', apis.RegistrationList.as_view()),

]

