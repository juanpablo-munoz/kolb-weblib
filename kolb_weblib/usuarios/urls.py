from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout

app_name = 'usuarios'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^login_usuario/$', views.login_usuario,  name='inicio'),
    url(r'^panel/$', views.panel,  name='panel'),
    url(r'^logout_usuario/$', logout, {'template_name': 'usuarios/index.html'}, name='cerrar'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_usuario.as_view(), name='editar'),
]