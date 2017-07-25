from django.contrib.auth import authenticate, login, logout
from kolb_weblib.settings import USER_DIR
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect  # , get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'usuarios/index.html')


def panel(request):
    if request.method == "POST":
        accion = request.POST['accion']
        usuario = User.objects.get(username=request.POST['user_id'])
        if accion == "del":
            usuario.delete()
        elif accion == 'ban':
            usuario.is_active = False
            usuario.save()
        elif accion == 'unban':
            usuario.is_active = True
            usuario.save()
        miembros = User.objects.all()
        return render(request, 'usuarios/panel.html', {'miembros': miembros})
    else:
        if request.user.is_authenticated:
            miembros = User.objects.all()
            return render(request, 'usuarios/panel.html', {'miembros': miembros})
        else:
            return render(request, 'usuarios/index.html')
        



# Vista para cerrar sesion

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return render(request, 'usuarios/index.html')

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
    else:
        if request.user.is_authenticated:
            return render(request, 'usuarios/index.html')
        else:
            return render(request, 'usuarios/login.html')


# Vista para el registro


def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)  # Forma a utilizar
        context = {"form": form}
        if form.is_valid():  # Si se llenan los campos con valores validos
            form.save()
            return redirect('/')
        else:
            return render(request, USER_DIR+'templates/usuarios/registro.html', context)
    else:
        if request.user.is_authenticated:
            return render(request, 'usuarios/index.html')
        else:
            form = RegistrationForm(None)
            context = {"form": form}
            return render(request, USER_DIR + 'templates/usuarios/registro.html', context)




class edit_usuario(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'usuarios/edit.html'
    success_url = '/panel/'
    login_url = '/login_usuario/'