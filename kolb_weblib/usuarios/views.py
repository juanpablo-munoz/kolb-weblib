from django.contrib.auth import authenticate, login, logout
from kolb_weblib.settings import USER_DIR
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect  # , get_object_or_404
from .forms import UserForm, RegistrationForm
from django.urls import reverse
import os
from django.views.generic import CreateView


def index(request):
    return render(request, 'usuarios/index.html')


# Vista para cerrar sesion

def logout_usuario(request):
    logout(request)  # Funcion especial de django
    return render(request, 'usuarios/index.html')  # Una vez cerrada la sesion redirige a la pantalla de inicio


# Vista para iniciar sesion


def login_usuario(request):
    if request.method == "POST":  # Si completa todos os campos
        username = request.POST['username']  # Obtiene el usuario
        password = request.POST['password']  # Obtiene la contraseña
        user = authenticate(username=username, password=password)  # Verifica si usuario esta en la BD.
        if user is not None:  # Si usuario existe
            if user.is_active:  # Si usuario no esta baneado
                login(request, user)  # Iniciar sesion
                return render(request, USER_DIR+'templates/usuarios/index.html')
            else:  # Si usuario esta baneado
                return render(request, USER_DIR+'templates/usuarios/login.html', {'error_message': 'Tu cuenta ha sido desactivada'})
        else:  # Si usuario no existe
            return render(request, USER_DIR+'templates/usuarios/login.html', {'error_message': 'Inicio de sesión falló'})
    return render(request, USER_DIR+'templates/usuarios/login.html')  # Si no completa todos los campos

# Vista para el registro


def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)  # Forma a utilizar
        if form.is_valid():  # Si se llenan los campos con valores validos
            form.save()
            return redirect('/usuarios')
        else:
            return redirect('/usuarios')
    else:
        form = RegistrationForm(None)
        context = {"form": form}
        return render(request, USER_DIR+'templates/usuarios/registro.html', context)
