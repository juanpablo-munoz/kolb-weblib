from django.conf.urls import url
from . import views

app_name='classifierapp'

urlpatterns = [
    url(r'^$', views.classifier_index, name='classifier_index'),
    url(r'^manual_classification$', views.manual_classification, name='manual_classification'),
    url(r'^automatic_classification$', views.automatic_classification, name='automatic_classification'),
    url(r'^create_classifier$', views.create_classifier, name='create_classifier'),
    url(r'^train_classifier$', views.train_classifier, name='train_classifier'),
    url(r'^delete_classifier$', views.delete_classifier, name='delete_classifier'),
]
