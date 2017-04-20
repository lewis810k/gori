"""gori URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from member.urls import apis as member_api_urls
from member.urls import member as member_urls
from talent.urls import apis as talent_api_urls
from talent.urls import talent as talent_urls

# ##### API URL #####
api_urlpatterns = [
    url(r'^member/', include(member_api_urls, namespace='member')),
    url(r'^talent/', include(talent_api_urls, namespace='talent')),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    # ##### API #####
    url(r'^api/', include(api_urlpatterns, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    # ##### 일반 뷰에 대한 URL #####
    url(r'^member/', include(member_urls)),
    url(r'^main/', include(talent_urls)),
    url(r'^talent/', include(talent_urls)),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
