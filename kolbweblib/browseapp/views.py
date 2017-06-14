from django.shortcuts import render
import sys
from django.shortcuts import HttpResponse
from browseapp.models import MaterialWebProcesado

def browse_index(request):
    sitios_fuente = MaterialWebProcesado.objects.order_by('titulo')
    context = {
        'todos_los_sitios': sitios_fuente,
    }
    return render(request, 'browseapp/index.html', context)

def render_webpage(request, sitio_a_visitar):
    return render(request, 'browseapp/index.html', {
        'todos_los_sitios': MaterialWebProcesado.objects.order_by('titulo'),
        'url_a_visitar': sitio_a_visitar,
    })




