from django.conf.urls import url
from .. import views

# app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^my-page/$', views.my_page_view, name='my_page'),
]
