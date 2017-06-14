from django.db import models

class Pregunta(models.Model):
    #texto: contenido de la pregunta
    texto = models.CharField(max_length=250)    
    #respuestaN: priorizacion entre 1 y 4 de las cuatro alternativas
    alternativa1 = models.CharField(max_length=1)
    alternativa2 = models.CharField(max_length=1)
    alternativa3 = models.CharField(max_length=1)
    alternativa4 = models.CharField(max_length=1)

# cada pregunta tendrá cuatro alternativas.
class Alternativa(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    # texto: el texto que describe la alternativa a la pregunta
    texto = models.CharField(max_length=250)
