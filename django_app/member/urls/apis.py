from django.conf.urls import url, include

from .. import apis

urlpatterns = [
    # ##### 회원가입 #####
    # 페이스북은 유저생성과 로그인을 fb_login에서 일괄적으로 처리함
    url(r'^signup/$', apis.CreateDjangoUserView.as_view()),

    # ##### 유저정보 보기 #####
    url(r'^profile/tutor/$', apis.TutorProfileView.as_view()),
    url(r'^profile/user/$', apis.UserProfileView.as_view(), name='user-detail'),

    # ##### 정보수정 #####
    url(r'^update/user/$', apis.UserProfileView.as_view(), name='user-patch'),

    # ##### 유저삭제 #####
    url(r'^delete/user/$', apis.UserProfileView.as_view(), name='user-delete'),

    # ##### 로그인/로그아웃 #####
    url(r'^fb_login/$', apis.CreateFacebookUserView.as_view()),
    url(r'^logout/$', apis.CustomLogoutView.as_view()),

    # ##### 마이페이지 관련 #####
    url(r'^wish-list/$', apis.MyWishListView.as_view()),
    url(r'^registrations/$', apis.MyRegistrationView.as_view()),

    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # rest_auth.urls에 login, logout, user, password 등의 뷰가 존재함.
    # /api/member/login 식으로 들어올 때 여기로 이동함.
    url(r'^', include('rest_auth.urls')),

    # ##### 토큰 #####
    url(r'^token-auth/$', apis.ObtainAuthToken.as_view()),
]
