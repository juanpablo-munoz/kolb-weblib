from django.shortcuts import render
import sys
from django.shortcuts import HttpResponse
from browseapp.models import MaterialWebProcesado

def crawl_index(request):
    sitios_fuente = MaterialWebProcesado.objects.order_by('titulo')
    context = {
        'sitios_fuente': sitios_fuente,
    }
    return render(request, 'crawlerapp/index.html', context)

def return_console_output(f):
    class WritableObject:
        def __init__(self):
            self.content = []
        def write(self, string):
            self.content.append(string)

    def new_f(*args, **kwargs):
        printed = WritableObject()
        sys.stdout = printed
        f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        context = {
            'sitios_fuente': MaterialWebProcesado.objects.order_by('titulo'),
            'console_output': ''.join(printed.content).split('\n'),
        }
        return render(args, 'crawlerapp/index.html', context)

#@return_console_output
def run_crawler(request):
    try:
        nuevo_sitio_fuente = request.POST['nuevo_sitio_fuente']
        profundidad = request.POST['depth']
    except:
        return render(request, 'crawlerapp/index.html', {
            'sitios_fuente': MaterialWebProcesado.objects.order_by('titulo'),
            'error': 'Error al intentar explorar la URL.'
        })

    class WritableObject:
        def __init__(self):
            self.content = []
        def write(self, string):
            self.content.append(string)

    import re
    from .crawler import Crawler, CrawlerCache
    crawler = Crawler(CrawlerCache(), depth=int(profundidad))
    root_re = re.compile('^/$').match
    sitios_explorados = WritableObject()
    sys.stdout = sitios_explorados #redirige el lo que se imprime en la consola hacia la variable console_output
    crawler.crawl(nuevo_sitio_fuente, no_cache=root_re)
    sys.stdout = sys.__stdout__ #restaura la salida por consola
    context = {
        'sitios_fuente': MaterialWebProcesado.objects.order_by('titulo'),
        'nuevo_sitio_fuente': nuevo_sitio_fuente,
        'sitios_explorados': ''.join(sitios_explorados.content).split('\n'),
        'profundidad': profundidad,
    }
    return render(request, 'crawlerapp/index.html', context)











