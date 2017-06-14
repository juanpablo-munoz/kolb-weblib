from django.shortcuts import render
from django.http import HttpResponse

def test_index(request):
    return HttpResponse("<h1>Página principal del Test de Estilos de Aprendizaje.</h1>")
