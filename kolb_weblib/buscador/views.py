from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import UserForm


def index(request):
    return render(request, 'buscador/index.html') 


# Vista para cerrar sesion

def logout_usuario(request):
    logout(request) # Funcion especial de django
    return render(request, 'buscador/index.html') #Una vez cerrada la sesion redirige a la pantalla de inicio


# Vista para iniciar sesion	
	
def login_usuario(request):
    if request.method == "POST": # Si completa todos os campos
        username = request.POST['username'] # Obtiene el usuario
        password = request.POST['password'] # Obtiene la contraseña
        user = authenticate(username=username, password=password) # Verifica si usuario esta en la BD.
        if user is not None: # Si usuario existe 
            if user.is_active: # Si usuario no esta baneado
                login(request, user) # Iniciar sesion
                return render(request, 'buscador/index.html')
            else: # Si usuario esta baneado
                return render(request, 'buscador/login.html', {'error_message': 'Tu cuenta ha sido desactivada'})
        else: # Si usuario no existe
            return render(request, 'buscador/login.html', {'error_message': 'Inicio de sesión falló'})
    return render(request, 'buscador/login.html') # Si no completa todos los campos

# Vista para el registro
							
def registro(request):
	form = UserForm(request.POST or None) # Forma utilizar
	if form.is_valid(): # Si se llenan los campos con valores validos
		user = form.save(commit=False) # Se crea un contenedor con los datos del usuario
		username = form.cleaned_data['username'] # Se limpia el input
		password = form.cleaned_data['password'] # Lo mismo
		user.set_password(password) # Guarda la contraseña
		user.save() # Guarda usuario en la base de datos
		user = authenticate(username=username, password=password) # Verifica si usuario esta en la BD.
		if user is not None: # Si usuario existe 
			if user.is_active:  # Si usuario no esta baneado
				login(request, user) # Iniciar sesion
				return render(request, 'buscador/index.html')
	context = {"form": form,}
	return render(request, 'buscador/registro.html', context)
	