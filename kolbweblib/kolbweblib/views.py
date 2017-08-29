from django.shortcuts import render

def home(request):
    context = {
        'mensaje': 'Bienvenido a KolbWebLib!',
        'version': 'Alpha v1.0.0',
        'funcionalidades': ['Crawling desde URL entregada a mano',
                            'Browsing basico de sitios Web (clic en el logo en la esquina sup. izq.)',
                            'Filtrado de texto desde codigo fuente, en preparacion para pasarlo a un clasificador.',
                            'Gestion CRUD basico sobre contenido Web explorado (dirigirse a localhost:8000/admin/ con user \'admin\' y clave \'kolb2017\' para comprobar este punto y el anterior).',
                            'NUEVO: Implementacion de clasificador neuronal multicategorico para el texto de las paginas Web almacenadas.',

                            ]
    }
    return render(request, 'kolbweblib/home.html', context)
