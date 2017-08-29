from django.db import models
from django.template.defaultfilters import truncatewords_html
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

class MaterialWebProcesado(models.Model):
    dominio = models.URLField(_('dominio'), max_length=255, default='Sin Dominio')
    url = models.URLField(_('url'), max_length=1000)
    titulo = models.CharField(_('titulo'), max_length=255)
    idioma = models.CharField(_('idioma'), max_length=10)
    tipo_aprendizaje = models.CharField(_('tipo_aprendizaje'), max_length=10)
    contenido = models.TextField(_('contenido'))
    codigo_fuente = models.TextField(_('codigo_fuente'), default='')

    class Meta:
        verbose_name = _('Material Web Procesado')
        verbose_name_plural = _('Materiales Web Procesados')

    def __str__(self):
        return self.titulo

    def __repr__(self):
        return '<MaterialWebProcesado: %s -- %s>' % (self.titulo, truncatewords_html(self.contenido, 10))

    def __unicode__(self):
        return force_text(self.__repr__())

    def get_absolute_url(self):
        return self.url
