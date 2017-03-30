from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^list/$', apis.TalentList.as_view()),

]
