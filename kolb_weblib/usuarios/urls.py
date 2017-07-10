from django.conf.urls import url
from . import views

app_name = 'usuarios'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^login_usuario/$', views.login_usuario, name='login_usuario'),
    url(r'^logout_usuario/$', views.logout_usuario, name='logout_usuario'),
]