from django.conf.urls import url

from member import apis as m_apis
from .. import apis

app_name = 'talent'

urlpatterns = [
    # url(r'^list/location/$', apis.LocationList.as_view()),
    # url(r'^wishlist/$', apis.WishList.as_view()),

    # ##### 생성 #####
    url(r'^create/$', apis.TalentListCreateView.as_view(), name='create'),
    url(r'^add/class-image/$', apis.ClassImageListCreateView.as_view(), name='class-image-create'),
    url(r'^add/location/$', apis.LocationCreateView.as_view(), name='location-create'),
    url(r'^add/curriculum/$', apis.CurriculumListCreateView.as_view(), name='curriculum-create'),
    url(r'^add/registration/$', apis.RegistrationListCreateView.as_view(), name='registration-create'),
    url(r'^add/review/$', apis.ReviewCreateView.as_view(), name='review-create'),
    url(r'^add/question/$', apis.QuestionCreateView.as_view(), name='question-create'),
    url(r'^add/reply/$', apis.ReplyCreateView.as_view(), name='reply-create'),

    # ##### 삭제 #####
    url(r'^delete/question/$', apis.QuestionDeleteView.as_view()),

    # ##### 리스트 #####
    url(r'^list/$', apis.TalentListCreateView.as_view(), name='list'),
    url(r'^list/unverified/$', apis.UnverifiedTalentListView.as_view(), name='list-unverified'),

    # ##### 전체보기 #####
    url(r'^detail-all/(?P<pk>[0-9]+)/$', apis.TalentDetailView.as_view(), name='detail-all'),

    # ##### 요약 #####
    url(r'^detail/(?P<pk>[0-9]+)/$', apis.TalentShortDetailView.as_view(), name='detail-short'),
    url(r'^detail/(?P<pk>[0-9]+)/location/$', apis.LocationListCreateView.as_view(), name='location-retrieve'),
    url(r'^detail/(?P<pk>[0-9]+)/class-image/$', apis.ClassImageListCreateView.as_view(), name='classimage-retrieve'),
    url(r'^detail/(?P<pk>[0-9]+)/curriculum/$', apis.CurriculumListCreateView.as_view(), name='curriculum-retrieve'),
    url(r'^detail/(?P<pk>[0-9]+)/registration/$', apis.RegistrationListCreateView.as_view(),
        name='registration-retrieve'),
    url(r'^detail/(?P<pk>[0-9]+)/review/$', apis.ReviewListView.as_view(), name='review-retrieve'),
    url(r'^detail/(?P<pk>[0-9]+)/qna/$', apis.QnATalentListView.as_view(), name='qna-retrieve'),

    # ##### 위시리스트 추가/삭제 #####
    url(r'^(?P<pk>[0-9]+)/wish-list/toggle/$', m_apis.WishListToggleView.as_view(), name='wishlist-toggle'),
    url(r'^(?P<pk>[0-9]+)/sales-status/toggle/$', apis.TalentSalesStatusToggleView.as_view(), name='sales-toggle'),
    # url(r'^registration/$', apis.RegistrationList.as_view()),
]
