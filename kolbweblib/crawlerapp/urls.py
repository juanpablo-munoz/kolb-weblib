from django.conf.urls import url
from . import views

app_name='crawlerapp'

urlpatterns = [
    url(r'^$', views.crawl_index, name='crawl_index'),
    #url(r'^(?P<sitio_fuente>[\w]+)/(?P<profundidad>[12345])/$', views.run_crawler, name='run_crawler'),
    url(r'^run_crawler$', views.run_crawler, name='run_crawler'),
]
