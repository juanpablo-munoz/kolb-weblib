from django.contrib.auth import authenticate, login, logout
from kolb_weblib.settings import USER_DIR
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect  # , get_object_or_404
from .forms import RegistrationForm
from django.urls import reverse
import os
from django.views.generic import CreateView


def index(request):
    return render(request, 'usuarios/index.html')

def panel(request):
    return render(request, 'usuarios/panel.html')


# Vista para cerrar sesion

def logout_usuario(request):
    logout(request)  # Funcion especial de django
    return render(request, 'usuarios/index.html')  # Una vez cerrada la sesion redirige a la pantalla de inicio


# Vista para iniciar sesion

def login_usuario(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'usuarios/index.html')
            else:
                return render(request, 'usuarios/login.html', {'error_message': 'Tu cuenta ha sido deshabilitada'})
        else:
            return render(request, 'usuarios/login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos'})
    return render(request, 'usuarios/login.html')

# def login_usuario(request):
#     form = AuthenticationForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             user = form.login(request)
#             if user:
#                 login(request, user)
#                 return redirect('/usuarios')
#         else:
#             return render(request, USER_DIR + 'templates/usuarios/login.html', {'form': form})
#     else:
#         return render(request, USER_DIR+'templates/usuarios/login.html', {'form': form})

# Vista para el registro


def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)  # Forma a utilizar
        context = {"form": form}
        if form.is_valid():  # Si se llenan los campos con valores validos
            form.save()
            return redirect('/usuarios')
        else:
            return render(request, USER_DIR+'templates/usuarios/registro.html', context)
    else:
        form = RegistrationForm(None)
        context = {"form": form}
        return render(request, USER_DIR+'templates/usuarios/registro.html', context)
