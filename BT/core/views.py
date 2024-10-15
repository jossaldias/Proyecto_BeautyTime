import os
import requests

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
import json

from django.db.models import Q
from .models import *
from .forms import *

from .utils import render_to_pdf
from django.views.generic import View
from django.core.mail import send_mail

from datetime import timedelta, datetime


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

# FUNCIÓN PARA ACCEDER A LA AGENDA
def calendario(request):
    return render(request, 'agenda/calendario.html')

# FUNCIÓN PARA AGENDAR UNA CITA
def reservar_cita(request):
    reservas = Reserva.objects.all()
    
    if request.method == 'POST':
        form = ReservaCitaForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            contacto = form.cleaned_data['contacto']
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            servicio = form.cleaned_data['servicio']

            # Combinar fecha y hora
            fecha_hora_inicio = datetime.combine(fecha, hora)
            fecha_hora_fin = fecha_hora_inicio + timedelta(hours=1)

            # Verificar si la fecha/hora ya ha pasado
            if fecha_hora_inicio < datetime.now():
                form.add_error(None, 'No puedes agendar una cita en una fecha u hora pasada.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            # Verificar si la fecha/hora está dentro del horario laboral
            dia_semana = fecha_hora_inicio.weekday()  # 0 = Lunes, 6 = Domingo
            if dia_semana == 0 or dia_semana == 6:
                form.add_error(None, 'No puedes agendar citas los domingos o lunes, ya que estamos cerrados.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            if dia_semana in [1, 2, 3] and not (9 <= hora.hour < 17):
                form.add_error(None, 'El horario de atención de martes a jueves es de 9:00 a 17:00.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            if dia_semana == 4 and not (9 <= hora.hour < 19):
                form.add_error(None, 'El horario de atención los viernes es de 9:00 a 19:00.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            if dia_semana == 5 and not (8 <= hora.hour < 16):
                form.add_error(None, 'El horario de atención los sábados es de 8:00 a 16:00.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            # Verificar si ya hay una reserva para el mismo servicio en la misma hora
            reserva_existente = Reserva.objects.filter(
                servicio=servicio,
                fecha=fecha,
                hora__lt=(fecha_hora_fin.time()),  # Compara con la hora final
                hora__gte=hora  # Compara con la hora de inicio
            )

            if reserva_existente.exists():
                form.add_error(None, 'Ya existe una reserva para este servicio en el horario seleccionado.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})

            # Crear una nueva reserva si no existe una en el mismo horario
            nueva_reserva = Reserva.objects.create(
                nombre=nombre,
                email=email,
                contacto=contacto,
                fecha=fecha,
                hora=hora,
                servicio=servicio
            )
            nueva_reserva.save()

            # Enviar correos de confirmación
            enviar_correos_confirmacion(nombre, email, fecha_hora_inicio, servicio)

            return redirect('reserva_exitosa')

    else:
        form = ReservaCitaForm()

    return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas})


# AGENDADO EXITOSAMENTE
def reserva_exitosa(request):
    return render(request, 'agenda/reserva_exitosa.html')

# ENVIAR CORREOS:
# FUNCIÓN PARA ENVIAR EL CORREO AL CLIENTE
def enviar_correo_cliente(nombre, email_cliente, fecha_hora_inicio, servicio):
    asunto = 'Confirmación de cita en BeautyTime'
    mensaje = f'Estimado {nombre},\n\n' \
              f'Tu cita para el servicio de {servicio} ha sido confirmada.\n' \
              f'Fecha y hora: {fecha_hora_inicio.strftime("%Y-%m-%d %H:%M")}\n\n' \
              f'Si tienes alguna consulta, no dudes en contactarnos.\n\n' \
              f'Saludos,\nBeautyTime'
    send_mail(
        asunto,
        mensaje,
        'beautytimeagenda@gmail.com',  # Remitente
        [email_cliente],  # Destinatario
        fail_silently=False,
    )

# FUNCIÓN PARA ENVIAR EL CORREO AL ADMINISTRADOR
def enviar_correo_admin(nombre, fecha_hora_inicio, servicio):
    asunto = 'Nueva cita agendada en BeautyTime'
    mensaje = f'Se ha agendado una nueva cita con el cliente {nombre}.\n\n' \
              f'Servicio: {servicio}\n' \
              f'Fecha y hora: {fecha_hora_inicio.strftime("%Y-%m-%d %H:%M")}\n\n' \
              f'Recuerda revisar el calendario para más detalles.\n\n' \
              f'Saludos,\nBeautyTime'
    send_mail(
        asunto,
        mensaje,
        'beautytimeagenda@gmail.com',  # Remitente
        ['beautytimeagenda@gmail.com'],  # Destinatario: administrador
        fail_silently=False,
    )

# FUNCIÓN PARA ENVIAR CORREOS DE CONFIRMACIÓN
def enviar_correos_confirmacion(nombre, email_cliente, fecha_hora_inicio, servicio):
    enviar_correo_cliente(nombre, email_cliente, fecha_hora_inicio, servicio)
    enviar_correo_admin(nombre, fecha_hora_inicio, servicio)


# FUNCIÓN PARA OBTENER RESERVAS
def obtener_reservas(request):
    servicio = request.GET.get('servicio')

    # Si no se proporciona un servicio, devolver todas las reservas (para el administrador)
    if servicio:
        reservas = Reserva.objects.filter(servicio__iexact=servicio)  # Filtro insensible a mayúsculas/minúsculas
    else:
        reservas = Reserva.objects.all()  # Devuelve todas las reservas si no se filtra por servicio

    reservas_data = [{
        'id': reserva.id,
        'nombre': reserva.nombre,
        'email': reserva.email,  # Agregando el email
        'contacto': reserva.contacto,  # Agregando el número de contacto
        'servicio': reserva.servicio,
        'fecha_inicio': datetime.combine(reserva.fecha, reserva.hora).isoformat(),
        'fecha_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).isoformat(),
    } for reserva in reservas]

    return JsonResponse({'reservas': reservas_data})

# Eliminar cita
#@login_required
def eliminar_cita(request, id):
    if request.method == 'POST':  # Aseguramos que sea un POST
        print(f"Solicitud de eliminación recibida para la cita con ID {id} con método {request.method}")
        try:
            # Obtener la cita a eliminar:
            reserva = get_object_or_404(Reserva, id=id)
            cliente_email = reserva.email
            cliente_nombre = reserva.nombre
            servicio = reserva.servicio
            fecha = reserva.fecha
            hora_formateada = reserva.hora.strftime("%H:%M")

            # Eliminar la cita
            reserva.delete()

            # Notificar al cliente de la cancelación por correo
            try:
                send_mail(
                    'Cancelación de su cita en BeautyTime',
                    f'Estimado/a {cliente_nombre}, lamentamos informarle que su cita para el servicio {servicio}, programada para el {fecha} a las {hora_formateada}, ha sido cancelada.\n\nGracias por confiar en BeautyTime.',
                    'beautytimeagenda@gmail.com',
                    [cliente_email],
                    fail_silently=False,
                )
                print(f"Correo de cancelación enviado a {cliente_email}")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

            return JsonResponse({'success': True})
        except Reserva.DoesNotExist:
            print(f"No se encontró la reserva con ID {id}")
            return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})
    else:
        print(f"Se recibió un método no permitido: {request.method}")
        return JsonResponse({'success': False, 'message': 'Método no permitido'})


# Editar cita
@login_required
def editar_cita(request, id):
    if request.method == 'POST':
        try:
            reserva = get_object_or_404(Reserva, id=id)
            data = json.loads(request.body)

            servicio = data.get('servicio')
            fecha = data.get('fecha')
            hora = data.get('hora')
            notify_client = data.get('notifyClient')  # Obtener si se debe notificar al cliente

            # Actualizar la reserva
            reserva.servicio = servicio
            reserva.fecha = fecha
            reserva.hora = hora
            reserva.save()

            # Si el administrador ha decidido notificar al cliente, enviamos el correo
            if notify_client:
                send_mail(
                    'Actualización de su cita en BeautyTime',
                    f'Estimado/a {reserva.nombre}, su cita ha sido modificada. Los detalles actualizados son:\n\n'
                    f'Servicio: {reserva.servicio}\nFecha: {reserva.fecha}\nHora: {reserva.hora}\n\nGracias por confiar en BeautyTime.',
                    'beautytimeagenda@gmail.com',
                    [reserva.email],
                    fail_silently=False,
                )

            return JsonResponse({'success': True})
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def obtener_servicios(request):
    servicios = ["Manicura", "Masaje", "Corte de Pelo", "Tinturado"]
    return JsonResponse({'servicios': servicios})

# FUNCIÓN PARA OBTENER LOS DETALLES DE UNA RESERVA ESPECÍFICA
def obtener_reserva(request, id):
    try:
        reserva = get_object_or_404(Reserva, id=id)
        reserva_data = {
            'id': reserva.id,
            'nombre': reserva.nombre,
            'email': reserva.email,
            'servicio': reserva.servicio,
            'fecha': reserva.fecha.isoformat(),
            'hora': reserva.hora.strftime("%H:%M"),
            'contacto': reserva.contacto  # Agregando el contacto
        }
        return JsonResponse(reserva_data)
    except Reserva.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})

#CARRITO
from django.shortcuts import render

def carrito(request):
    return render(request, 'tienda/carrito.html')  


#ATENCION CLIENTE

def atencioncliente(request):
    return render(request, 'tienda/atencioncliente.html')