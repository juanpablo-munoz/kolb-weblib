import datetime
from haystack import indexes
from browseapp.models import MaterialWebProcesado


class MaterialWebProcesadoIndex(indexes.SearchIndex, indexes.Indexable):
    dominio = indexes.CharField(model_attr='dominio')
    url = indexes.CharField(model_attr='url')
    titulo = indexes.DateTimeField(model_attr='titulo')
    idioma = indexes.CharField(model_attr='idioma')
    tipo_aprendizaje = indexes.CharField(model_attr='tipo_aprendizaje')
    contenido = indexes.CharField(model_attr='contenido')
    documento = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return MaterialWebProcesado

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()