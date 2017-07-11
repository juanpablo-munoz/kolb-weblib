from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'usuarios'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^login_usuario/$', login, {'template_name': 'usuarios/login.html'}, name='login_usuario'),
    url(r'^logout_usuario/$', views.logout_usuario, name='logout_usuario'),
]