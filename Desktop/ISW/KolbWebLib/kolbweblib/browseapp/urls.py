from django.conf.urls import url
from . import views

app_name='browseapp'

urlpatterns = [
    url(r'^$', views.browse_index, name='browse_index'),
    #url(r'^(?P<sitio_fuente>[\w]+)/(?P<profundidad>[12345])/$', views.run_crawler, name='run_crawler'),
    url(r'^=(?P<sitio_a_visitar>(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?)$', views.render_webpage, name='render_webpage'),
]