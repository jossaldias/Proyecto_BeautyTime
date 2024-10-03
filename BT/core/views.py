import os
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from django.db.models import Q
from .models import *
from .forms import *

# HOME


def home(request):
    print(request.session.session_key)

    return render(request, "base/home.html", {"home": home})


def login(request):
    print(request.session.session_key)

    return render(request, "registration/login.html", {"login": login})


# PERFILES


# REGISTRARSE
def register(request):
    data = {"form": CustomUserCreationForm()}

    if request.method == "POST":
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(
                username=user_creation_form.cleaned_data["username"],
                password=user_creation_form.cleaned_data["password1"],
            )
            login(request, user)

            return redirect("home")

    return render(request, "registration/register.html", data)


# VER PERFIL PROPIO
@login_required
def perfil(request):
    form = editarPerfilForm()
    context = {"form": form}
    return render(request, "registration/perfil.html", context)


# EDITAR PERFIL PROPIO
@login_required
def editarPerfil(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.POST.get("id_perfil_editar"))
        form = editarPerfilForm(
            data=request.POST, files=request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
        return redirect("perfil")
    else:
        form = editarPerfilForm()
        context = {"form": form}
    return render(request, "paginas/perfil.html", context)


# EDITAR USUARIO DESDE ADMINISTRADOR GENERAL
@login_required
def editarUsuario(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.POST.get("id_usuario_editar"))
        form_editar = editarUsuarioForm(
            data=request.POST, files=request.FILES, instance=user
        )
        if form_editar.is_valid():
            form_editar.save()

        return redirect("usuarios")
    else:
        form_editar = editarUsuarioForm()
        context = {"form_editar": form_editar}
    return render(request, "paginas/usuarios.html", context)


# FUNCIÓN PARA SALIR DE LA SESIÓN DEL USUARIO
def exit(request):
    logout(request)
    return redirect("home")


# FUNCIÓN PARA EL ADMINISTRADOR GENERAL PARA LA GESTIÓN DE USUARIOS
@login_required
def usuarios(request):
    users = User.objects.all()
    form_editar = editarUsuarioForm()
    context = {"users": users, "form_editar": form_editar}

    return render(request, "registration/usuarios.html", context)


# FUNCIÓN PARA EL ADMINISTRADOR GENERAL PARA  AGREGAR UN USUARIO
@login_required
def agregarUsuario(request):

    if request.method == "POST":
        form = editarUsuarioForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect("usuarios")
    else:
        form = editarUsuarioForm()
        context = {"form": form}
    return render(request, "registration/agregarUsuario.html", context)


# FUNCIÓN PARA EL ADMINISTRADOR GENERAL PARA ELIMINAR UN USUARIO
@login_required
def eliminarUsuario(request):
    if request.POST:
        users = User.objects.get(pk=request.POST.get("id_usuario_eliminar"))
        users.delete()

    return redirect("usuarios")


def servicios(request):    
    servicios = Item.objects.filter(
                                    Q(tipo='servicio') & 
                                    (Q(categoria='Manicure y Pedicure') | 
                                     Q(categoria='Masajes') | 
                                     Q(categoria='Maquillaje para eventos') | 
                                     Q(categoria='Depilación') | 
                                     Q(categoria='Tratamientos Faciales') | 
                                     Q(categoria='Colorimetría'))
                                    )
    context = {
        'servicios': servicios
    }
    return render(request, 'tienda/servicios.html', context)

def productos(request):    
    productos = Item.objects.filter(
                                    Q(tipo='producto') & 
                                    (Q(categoria='Coloración') | 
                                     Q(categoria='Tratamientos') | 
                                     Q(categoria='Línea Rubias') | 
                                     Q(categoria='Shampoo & Acondicionadores') | 
                                     Q(categoria='Styling & Aftercare') | 
                                     Q(categoria='Herramientas'))
                                    )
    context = {
        'productos': productos
    }
    return render(request, 'tienda/productos.html', context)