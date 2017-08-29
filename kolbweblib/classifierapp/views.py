from django.shortcuts import render
from django.shortcuts import HttpResponse
from browseapp.models import MaterialWebProcesado

from keras.models import Sequential, load_model
from keras.layers import Dense
from django.core import serializers
import os
import numpy as np

from . import preprocesador

def classifier_index(request):
    # Carga las paginas Web almacenadas localmente
    sitios_fuente = MaterialWebProcesado.objects.order_by('titulo')

    # Cuenta la cantidad de documentos Web sin clasificar
    '''
    sitios_fuente_iterable = serializers.serialize("python", sitios_fuente)
    clasificados = 0
    total = 0
    for doc in sitios_fuente_iterable:
        total += 1
        for k, v in doc['fields'].items():
            if k == 'tipo_aprendizaje' and v == '':
                continue
        clasificados += 1
    sin_clasificar = total - clasificados
    '''
    # Intenta cargar algun modelo clasificador preexistente
    context = {
        'sitios_fuente': sitios_fuente,
        'clasificador_no_existe': not os.path.exists('classifierapp/clasificador.h5'),
    }
    return render(request, 'classifierapp/index.html', context)

def manual_classification(request):
    try:
        for url_doc in request.POST.keys():
            updateado = MaterialWebProcesado.objects.get(url=url_doc)
            if updateado.tipo_aprendizaje == request.POST[url_doc]:
                updateado.tipo_aprendizaje = ''
            else:
                updateado.tipo_aprendizaje = request.POST[url_doc]
            updateado.save()
    except:
        pass
    return classifier_index(request)

def create_classifier(request):
    try:
        # Definicion del clasificador
        modelo = Sequential()
        modelo.add(Dense(int(request.POST['num_neuronas_1']),
                            activation='relu',
                            input_shape=(500,)))
        modelo.add(Dense(int(request.POST['num_neuronas_2']),
                            activation='relu',))
        modelo.add(Dense(4, activation='softmax'))

        # Compilacion del clasificador
        modelo.compile(optimizer='rmsprop',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])

        # Guardar modelo en disco
        modelo.save('classifierapp/clasificador.h5')
        print('Clasificador guardado con exito')
        error = False
    except:
        error = 'No se pudo crear el clasificador.'
        modelo = None
    context = {
        'sitios_fuente': MaterialWebProcesado.objects.order_by('titulo'),
        'clasificador_no_existe': modelo is None,
        'clasificador_recien_creado': True,
        'error': error
    }
    return render(request, 'classifierapp/index.html', context)

def delete_classifier(request):
    os.remove('classifierapp/clasificador.h5')
    return classifier_index(request)

def train_classifier(request):
    # Crear dataset
    clases = []
    datos_completos = []
    datos_entrenamiento = []
    indices_datos_entrenamiento = []
    for index, doc in enumerate(list(MaterialWebProcesado.objects.order_by('titulo'))):
        datos_completos.append(doc.contenido)
        if doc.tipo_aprendizaje != '':
            clases.append(preprocesador.vectorizar_clase(doc.tipo_aprendizaje))
            indices_datos_entrenamiento.append(index)
    clases = np.array(clases)
    datos = preprocesador.vectorizer.fit_transform(datos_completos).toarray()
    for elem in indices_datos_entrenamiento:
        datos_entrenamiento.append(datos[elem])
    datos_entrenamiento = np.array(datos_entrenamiento)

    # Cargar modelo
    try:
        modelo = load_model('classifierapp/clasificador.h5')
    except:
        return render(request, 'classifierapp/index.html', {'error': 'No se pudo cargar el clasificador.'})
    # Entrenar modelo
    resultados = modelo.fit(x=datos_entrenamiento, y=clases, epochs=10)
    # Guardar modelo
    modelo.save('classifierapp/clasificador.h5')
    return render(request, 'classifierapp/index.html',
        {
            'resultados': round(resultados.history['acc'][-1]*100, 2),
            'sitios_fuente': MaterialWebProcesado.objects.order_by('titulo'),
            'clasificador_no_existe': False,
            'clasificador_recien_creado': False,
        })

def automatic_classification(request):
    # Crear dataset
    datos_completos = []
    urls = {}
    for index, doc in enumerate(list(MaterialWebProcesado.objects.order_by('titulo'))):
        datos_completos.append(doc.contenido)
        urls[doc.url] = index
    datos = np.array(preprocesador.vectorizer.fit_transform(datos_completos).toarray())

    # Cargar modelo
    try:
        modelo = load_model('classifierapp/clasificador.h5')
    except:
        return render(request, 'classifierapp/index.html', {'error': 'No se pudo cargar el clasificador.'})
    #try:
    for k, v in request.POST.items():
        if v != 'Autom.':
            continue
        updateado = MaterialWebProcesado.objects.get(url=k)
        print('Iniciando clasificador')
        prediccion = modelo.predict(datos[urls[k]].reshape((1, 500)), batch_size=1, verbose=1)
        updateado.tipo_aprendizaje = preprocesador.vector_a_clase(prediccion)
        print('Clasificacion:', updateado.tipo_aprendizaje)
        updateado.save()
    #except:
        pass
    return classifier_index(request)


        
        
        
