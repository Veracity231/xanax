from django.conf.urls import url
from . import views

app_name = 'display'

urlpatterns = [
    # /display/
    url(r'^$', views.index, name='main-view'),
    url(r'^index/$', views.index, name='index'),
    url(r'^check_api/$', views.check_api, name='check_api'),
    url(r'^show_all_members/$', views.show_all_members, name='show_all_members'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_screen/$', views.login_screen, name='login_screen'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]
