import os
import requests

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash

from django.db.models import Q
from .models import *
from .forms import *

from .utils import render_to_pdf
from django.views.generic import View


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
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})



# VER PERFIL PROPIO
@login_required
def perfil(request):
    form = editarPerfilForm()
    context = {"form": form}
    return render(request, "registration/perfil.html", context)


# EDITAR PERFIL PROPIO
@login_required
def editarPerfil(request):
    user = request.user
    
    if request.method == "POST":
        form = editarPerfilForm(data=request.POST, files=request.FILES, instance=user)
        
        if form.is_valid():
            if form.cleaned_data.get('password'):  
                user.set_password(form.cleaned_data['password']) 
            form.save()  
            messages.success(request, 'Perfil actualizado correctamente.')  
            return redirect("perfil")
    else:
        form = editarPerfilForm(instance=user)  

    context = {"form": form}
    return render(request, "paginas/perfil.html", context)


# EDITAR USUARIO DESDE ADMINISTRADOR GENERAL
@login_required
def editarUsuario(request):
    user = get_object_or_404(User, pk=request.POST.get("id_usuario_editar") if request.method == "POST" else request.GET.get("id_usuario_editar"))
    
    if request.method == "POST":
        form_editar = editarUsuarioForm(data=request.POST, files=request.FILES, instance=user)
        
        if form_editar.is_valid():
            password = form_editar.cleaned_data.get('password')  
            if password:  
                user.set_password(password)  
            form_editar.save()  
            messages.success(request, 'Usuario actualizado correctamente.')  
            return redirect("usuarios")
    else:
        form_editar = editarUsuarioForm(instance=user)  

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

def verDetalle(request, tipo, id):
    if tipo not in ['producto', 'servicio']:
        return render(request, '404.html') 
    item = get_object_or_404(Item, iditem=id)
    if item.tipo != tipo:
        return render(request, '404.html')  
    context = {
        'item': item,
        'tipo': tipo
    }
    return render(request, 'tienda/verDetalle.html', context)

class verInventario(View):

    def get(self, request, *args, **kwargs):
        productos = Item.objects.all()
        
        form_editar = editarProductoForm()

        context = {
            'productos': productos,
            'form_editar': form_editar,
        }
        
        if 'pdf' in request.GET:
            pdf = render_to_pdf('inventario/verInventario.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        return render(request, 'inventario/verInventario.html', context)

#FUNCION PARA VER STOCK DE PRODUCTOS
@login_required
def inventarioProducto(request):
    productos = Item.objects.all()
    form_editar = editarProductoForm()
    context = {
        'productos': productos,
        'form_editar':form_editar
    }
  
    return render(request, 'inventario/inventario.html', context)

#FUNCIÓN PARA AGREGAR PRODUCTO NUEVO A LA BASE DE DATOS
@login_required
def agregarProducto(request):
    if request.method == 'POST':
        form = agregarProductoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
    else:
        form = agregarProductoForm()
    
    context = {
        'form': form
    }
    print(context)
    return render(request, 'inventario/agregarProducto.html', context)

#FUNCIÓN PARA EDITAR PRODUCTO
@login_required
def editarProducto(request):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=request.POST.get('id_producto_editar'))
        form_editar = editarProductoForm(data=request.POST, files=request.FILES, instance=producto)
        if form_editar.is_valid():
            form_editar.save()
        return redirect('inventario')
    else:
        form_editar = editarProductoForm()
        context = {
            'form_editar': form_editar
        }
    return render(request, 'inventario/inventario.html', context)

#FUNCIÓN PARA ELIMINAR PRODUCTO
@login_required
def eliminarProducto(request):
  if request.method == 'POST':
        id_producto_eliminar = request.POST.get('id_producto_eliminar')
        producto = Producto.objects.get(pk=id_producto_eliminar)

        codigos = Codigo.objects.filter(producto_id=id_producto_eliminar)

        codigos.delete()

        producto.delete()

        return redirect('inventario')