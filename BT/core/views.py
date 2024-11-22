import os
import requests
import time
import string

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
import json

from django.db.models import Q, F, Sum, Count

from .utils import render_to_pdf
from django.views.generic import View, CreateView
from django.core.mail import send_mail

from datetime import timedelta, datetime
from django.contrib.auth.models import AnonymousUser


from .models import *
from .forms import *
from .cart import Cart

from .models import Producto, Categoria

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

            # Guardar cambios en el perfil
            user = form.save(commit=False)

            # Obtener el valor del campo de contraseña
            password = form.cleaned_data.get('password')

            # Solo cambiar la contraseña si el usuario ingresó una nueva
            if password:
                user.set_password(password)  # Encripta y actualiza la contraseña si hay una nueva
                update_session_auth_hash(request, user)  # Mantener la sesión si la contraseña se cambia

            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect("perfil")
        else:
            messages.error(request, 'Error al actualizar el perfil. Revisa los campos obligatorios.')
    else:
        form = editarPerfilForm(instance=user)
    
    context = {"form": form}
    return render(request, "registration/perfil.html", context)


# EDITAR USUARIO DESDE ADMINISTRADOR GENERAL
@login_required
def editarUsuario(request):
    # Obtener el usuario que se va a editar
    user = get_object_or_404(User, pk=request.POST.get("id_usuario_editar") if request.method == "POST" else request.GET.get("id_usuario_editar"))

    if request.method == "POST":
        # Creamos el formulario con los datos enviados
        form_editar = editarUsuarioForm(data=request.POST, files=request.FILES, instance=user)

        if form_editar.is_valid():
            # Guardamos los demás cambios
            user = form_editar.save(commit=False)

            # Comprobamos si la contraseña fue proporcionada
            password = form_editar.cleaned_data.get('password')

            # Si la contraseña no está vacía, la actualizamos
            if password:
                user.set_password(password)

            # Guardamos los cambios en el usuario
            user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect("usuarios")
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form_editar = editarUsuarioForm(instance=user)

    context = {"form_editar": form_editar}
    return render(request, "registration/usuarios.html", context)



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
        form = CustomUserCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario agregado correctamente.")
            return redirect("usuarios")
        else:
            messages.error(request, "Error al agregar el usuario. Verifica los datos.")
    else:
        form = CustomUserCreationForm()
    
    context = {"form": form}
    return render(request, "registration/agregarUsuario.html", context)

# FUNCIÓN PARA EL ADMINISTRADOR GENERAL PARA ELIMINAR UN USUARIO
@login_required
def eliminarUsuario(request):
    if request.method == "POST":
        user_id = request.POST.get("id_usuario_eliminar")
        if not user_id:
            messages.error(request, "No se proporcionó un ID válido para eliminar.")
            return redirect("usuarios")
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            messages.success(request, "Usuario eliminado correctamente.")
        except User.DoesNotExist:
            messages.error(request, "El usuario no existe.")
        except ValueError:
            messages.error(request, "ID de usuario inválido.")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
    return redirect("usuarios")



def servicios(request):    
    servicios = Item.objects.filter(tipo='servicio')
    context = {
        'servicios': servicios
    }
    return render(request, 'tienda/servicios.html', context)

def productos(request):    
    productos = Item.objects.filter(tipo='producto')
    context = {
        'productos': productos
    }
    return render(request, 'tienda/productos.html', context)

def verDetalle(request, id):
    item = get_object_or_404(Item, id=id)
    context = {
        'item': item,
        'tipo': item.tipo,
    }
    return render(request, 'tienda/verDetalle.html', context)

class verInventario(View):

    def get(self, request, *args, **kwargs):
        productos = Item.objects.filter(tipo='producto')
        form = editarProductoForm()

        context = {
            'productos': productos,
            'form': form,
        }
        
        if 'pdf' in request.GET:
            pdf = render_to_pdf('inventario/verInventario.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        return render(request, 'inventario/verInventario.html', context)

#FUNCION PARA VER STOCK DE PRODUCTOS
@login_required
def inventarioProducto(request):
    productos = Producto.objects.all()
    form = editarProductoForm()
    context = {
        'productos': productos,
        'form':form
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
    producto = get_object_or_404(Producto, pk=request.POST.get("id_producto_editar") if request.method == "POST" else request.GET.get("id_producto_editar"))

    if request.method == 'POST':
        form = editarProductoForm(data=request.POST, instance=producto)

        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = editarProductoForm(instance=producto)
        context = {"form": form }
    return render(request, 'inventario/inventario.html', context)

#FUNCIÓN PARA ELIMINAR PRODUCTO
@login_required
def eliminarProducto(request):
  if request.method == 'POST':
        id_producto_eliminar = request.POST.get('id_producto_eliminar')
        producto = Producto.objects.get(pk=id_producto_eliminar)

        producto.delete()

        return redirect('inventario')

# FUNCIÓN PARA ACCEDER A LA AGENDA
def calendario(request):
    return render(request, 'agenda/calendario.html')

# FUNCIÓN PARA AGENDAR UNA CITA
def reservar_cita(request):
    reservas = Reserva.objects.all()

    # Verificar si el usuario está autenticado
    usuario_autenticado = request.user.is_authenticated

    # Prellenar los campos si el usuario está autenticado
    if usuario_autenticado:
        user = request.user
        nombre_usuario = f"{user.first_name.split()[0]} {user.last_name.split()[0]}" if user.first_name and user.last_name else ""
        email_usuario = user.email
        contacto_usuario = user.telefono
    else:
        nombre_usuario = ''
        email_usuario = ''
        contacto_usuario = ''
    
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
            categoria = servicio.categoria  # Obtener la categoría del servicio seleccionado

            # Combinar fecha y hora
            fecha_hora_inicio = datetime.combine(fecha, hora)
            fecha_hora_fin = fecha_hora_inicio + timedelta(hours=1)

            # Verificar si la fecha/hora ya ha pasado
            if fecha_hora_inicio < datetime.now():
                form.add_error(None, 'No puedes agendar una cita en una fecha u hora pasada.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas, 'usuario_autenticado': usuario_autenticado})

            # Verificar si la fecha/hora está dentro del horario laboral
            dia_semana = fecha_hora_inicio.weekday()  # 6 = Domingo
            if dia_semana == 6:
                form.add_error(None, 'No puedes agendar citas los domingos, ya que estamos cerrados.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas, 'usuario_autenticado': usuario_autenticado})

            if dia_semana in [0, 1, 2, 3, 4, 5] and not (10 <= hora.hour < 20):
                form.add_error(None, 'El horario de atención es de lunes a sábados de 10:00 a 20:00.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas, 'usuario_autenticado': usuario_autenticado})

            # Verificar si ya hay una reserva para la misma categoría en la misma hora
            reserva_existente = Reserva.objects.filter(
                servicio__categoria=categoria,
                fecha=fecha,
                hora__lt=(fecha_hora_fin.time()),  # Compara con la hora final
                hora__gte=hora  # Compara con la hora de inicio
            )

            if reserva_existente.exists():
                form.add_error(None, f'Ya existe una reserva para esta categoría ({categoria.nombre}) en el horario seleccionado.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas, 'usuario_autenticado': usuario_autenticado})

            # Verificar si el cliente autenticado ya tiene una reserva en otra categoría para el mismo horario
            if usuario_autenticado:
                conflicto_reserva = Reserva.objects.filter(
                    cliente=request.user,
                    fecha=fecha,
                    hora__lt=fecha_hora_fin.time(),
                    hora__gte=hora
                ).exclude(servicio__categoria=categoria)

                if conflicto_reserva.exists():
                    # Añadir el error al formulario para que se muestre en la plantilla
                    form.add_error(
                        None,  # Error general del formulario
                        'Ya tienes una reserva en otro servicio para el horario seleccionado. Por favor selecciona otra hora o pide modificar tu reserva en "Calendario" '
                    )
                    return render(request, 'agenda/reservar_cita.html', {
                        'form': form,
                        'reservas': reservas,
                        'usuario_autenticado': usuario_autenticado,
                        'nombre_usuario': nombre_usuario,
                        'email_usuario': email_usuario,
                        'contacto_usuario': contacto_usuario,
                    })


            # Crear una nueva reserva
            nueva_reserva = Reserva(
                nombre=nombre,
                email=email,
                contacto=contacto,
                fecha=fecha,
                hora=hora,
                servicio=servicio
            )

            # Si el usuario está autenticado, asignar el cliente
            if usuario_autenticado:
                nueva_reserva.cliente = request.user

            nueva_reserva.save()

            # Enviar correos de confirmación
            enviar_correos_confirmacion(nombre, email, fecha_hora_inicio, servicio)

            return redirect('reserva_exitosa')

    else:
        form = ReservaCitaForm()

    return render(request, 'agenda/reservar_cita.html', {
        'form': form, 
        'reservas': reservas, 
        'usuario_autenticado': usuario_autenticado,
        'nombre_usuario': nombre_usuario,
        'email_usuario': email_usuario,
        'contacto_usuario': contacto_usuario
    })

# AGENDADO EXITOSAMENTE
def reserva_exitosa(request):
    return render(request, 'agenda/reserva_exitosa.html')

# ENVIAR CORREOS:
# FUNCIÓN PARA ENVIAR EL CORREO AL CLIENTE
def enviar_correo_cliente(nombre, email_cliente, fecha_hora_inicio, servicio):
    categoria = servicio.categoria  # Obtener la categoría del servicio
    asunto = 'Confirmación de cita en BeautyTime'
    mensaje = f'Estimado/a {nombre},\n\n' \
              f'¡Su cita para el servicio {categoria.nombre} - {servicio.nombre} ha sido agendada con éxito!.\n' \
              f'Fecha y hora: {fecha_hora_inicio.strftime("%Y-%m-%d %H:%M")}\n' \
              f'Dirección: Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana.\n\n'\
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
    mensaje = f'Se ha agendado una nueva cita con el/la cliente {nombre}.\n\n' \
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


# FUNCIÓN PARA OBTENER RESERVAS (reservar_cita.html)
def obtener_reservas(request):
    categoria_id = request.GET.get('categoria')
    user = request.user
    contexto = request.GET.get('contexto', 'calendario')  # Se agrega 'calendario' por defecto
    mostrar_solo_proximas = request.GET.get('mostrarSoloProximas', 'false') == 'true'  # Verificar el parámetro de filtro de citas futuras

    # Si se proporciona una categoría, filtrar las reservas por los servicios de esa categoría
    if categoria_id:
        try:
            categoria_id = int(categoria_id)  # Convertir el ID a entero
            reservas = Reserva.objects.filter(servicio__categoria_id=categoria_id).exclude(estado='eliminado')  # Filtrar por la categoría del servicio y excluir las eliminadas
        except ValueError:
            return JsonResponse({'error': 'ID de categoría no válido'}, status=400)
    else:
        reservas = Reserva.objects.exclude(estado='eliminado')  # Excluir las reservas con estado 'eliminado'

    # Filtrar por fechas si el checkbox está marcado
    if mostrar_solo_proximas:
        hoy = datetime.today().date()
        reservas = reservas.filter(fecha__gte=hoy)  # Filtra las reservas con fecha igual o superior a hoy

    # Si el usuario es cliente y el contexto es 'calendario', mostramos solo sus citas
    if contexto == 'calendario' and user.tipo_user != 'Administrador':
        reservas = reservas.filter(cliente=user)

    reservas_data = [{
        'id': reserva.id,
        'categoria': reserva.servicio.categoria.nombre, 
        'nombre': reserva.nombre,
        'email': reserva.email,  
        'contacto': reserva.contacto,
        'servicio': reserva.servicio.nombre,
        'hora_inicio': reserva.hora.strftime("%H:%M"), 
        'hora_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).strftime("%H:%M"),
        'fecha_inicio': datetime.combine(reserva.fecha, reserva.hora).isoformat(),
        'fecha_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).isoformat(),
        'estado': reserva.estado
    } for reserva in reservas]

    return JsonResponse({'reservas': reservas_data})



# Eliminar cita
@login_required
def eliminar_cita(request, id):
    if request.method == 'POST':
        try:
            reserva = get_object_or_404(Reserva, id=id)

            cliente_email = reserva.email
            cliente_nombre = reserva.nombre
            servicio = reserva.servicio
            fecha = reserva.fecha
            hora_formateada = reserva.hora.strftime("%H:%M")

            # Cambiar el estado de la reserva a 'eliminado'
            reserva.estado = 'eliminado'
            reserva.save()

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
            return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})




# Editar cita
@login_required
def editar_cita(request, id):
    if request.method == 'POST':
        try:
            reserva = get_object_or_404(Reserva, id=id)
            data = json.loads(request.body)

            servicio = get_object_or_404(Servicio, id=data.get('servicio'))  # Obtener el servicio por ID
            categoria = servicio.categoria  # Obtener la categoría del servicio
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
                    f'Categoría: {categoria.nombre}\n'
                    f'Servicio: {servicio.nombre}\n'
                    f'Fecha: {reserva.fecha}\n'
                    f'Hora: {reserva.hora}\n'
                    f'Dirección: Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana\n'
                    f'\n\nGracias por confiar en BeautyTime.',
                    'beautytimeagenda@gmail.com',
                    [reserva.email],
                    fail_silently=False,
                )

            return JsonResponse({'success': True})
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def obtener_categorias(request):
    categorias = Categoria.objects.filter(items__tipo='servicio').distinct()
    categorias_data = [{'id': categoria.id, 'nombre': categoria.nombre} for categoria in categorias]
    return JsonResponse({'categorias': categorias_data})


def obtener_servicios(request):
    categoria_id = request.GET.get('categoria_id')
    if categoria_id:
        servicios = Item.objects.filter(tipo='servicio', categoria_id=categoria_id)
        servicios_data = [{'id': servicio.id, 'nombre': servicio.nombre} for servicio in servicios]
        return JsonResponse({'servicios': servicios_data})
    else:
        return JsonResponse({'error': 'Categoría no especificada'}, status=400)

# FUNCIÓN PARA OBTENER LOS DETALLES DE UNA RESERVA ESPECÍFICA (calendario.html)
@login_required
def obtener_reserva(request, id):
    user = request.user
    try:
        # Obtener la reserva por ID
        reserva = Reserva.objects.get(id=id)

        # Verificar si el usuario está autenticado
        if isinstance(user, AnonymousUser):
            return JsonResponse({'success': False, 'message': 'Debes iniciar sesión para ver esta reserva.'}, status=403)

        # Verificar si el usuario es cliente y solo puede ver sus propias reservas
        if user.tipo_user != 'Administrador' and reserva.cliente != user:
            return JsonResponse({'success': False, 'message': 'No tienes permiso para ver esta reserva.'}, status=403)

        # Preparar los datos de la reserva
        reserva_data = {
            'id': reserva.id,
            'categoria': reserva.servicio.categoria.id,
            'categoria_nombre': reserva.servicio.categoria.nombre,  # Se añade para mostrar el nombre de la categoría
            'servicio': reserva.servicio.id,
            'servicio_nombre': reserva.servicio.nombre,  # Se añade para mostrar el nombre del servicio
            'hora_inicio': reserva.hora.strftime("%H:%M"),
            'hora_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).strftime("%H:%M"),
            'fecha_inicio': datetime.combine(reserva.fecha, reserva.hora).isoformat(),
            'fecha_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).isoformat(),
            'nombre': reserva.nombre,
            'email': reserva.email,
            'contacto': reserva.contacto,
            'estado': reserva.estado,
            'es_admin': user.tipo_user == 'Administrador'  # Determina si es administrador para la lógica del frontend
        }

        return JsonResponse(reserva_data)

    except Reserva.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'}, status=404)

# Confirmar reservas ya sea por correo desde el cliente o por whatsapp desde el admin.
def confirmar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        try:
            # Confirmar la reserva desde el admin (por WhatsApp)
            reserva.estado = 'confirmado'
            reserva.save()
            print(f"Reserva {reserva_id} confirmada.")  # Agrega un print para verificar que el estado cambió
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al confirmar la reserva: {e}")  # Imprimir cualquier error durante el guardado
            return JsonResponse({'success': False, 'error': str(e)})

    elif request.method == 'GET':
        # Confirmación desde el cliente (por correo)
        if 'accion' in request.GET and request.GET['accion'] == 'confirmar':
            try:
                reserva.estado = 'confirmado'
                reserva.save()
                return render(request, 'agenda/confirmacion_exitosa.html', {'reserva': reserva})
            except Exception as e:
                print(f"Error al confirmar la reserva por cliente: {e}")
                return render(request, 'agenda/confirmacion_fallida.html', {'error': str(e)})
        else:
            # Si no se pasa la acción correctamente
            return render(request, 'agenda/confirmacion_fallida.html', {'error': 'Acción no válida.'})
    
    # Si el método no es GET o POST, devolver un error
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)



#CARRITO
from django.shortcuts import render

def carrito(request):
    return redirect('carrito')

#FUNCIÓN PARA AGREGAR UN PRODUCTO MÁS AL CARRITO CON BOTÓN +
def cart_add(request, producto_id):

  cart = Cart(request)
  producto = get_object_or_404(Item, id=producto_id, tipo='producto')  # Filtrar por tipo producto

  form = CartAddProductoForm(request.POST)
  if form.is_valid():
    cart_add = form.cleaned_data
    cart.add(
      producto=producto,
      cantidad=cart_add["cantidad"],
      override_cantidad=cart_add["override"]
    )

  return redirect("carrito")

#FUNCIÓN PARA DISMIUIR UN PRODUCTO MÁS AL CARRITO CON BOTÓN -
def cart_eliminar(request, producto_id):

  cart = Cart(request)
  producto = get_object_or_404(Producto, id=producto_id)
  cart.remove(producto)
  return redirect("carrito")

#FUNCIÓN PARA LIMPIAR EL CARRITO 
def cart_clear(request):
  cart = Cart(request)
  cart.clear()
  return redirect("carrito")

#FUNCIÓN QUE MUESTRA EL DETALLE DE LA COMPRA 
def cart_detalle(request):
  cart = Cart(request)
  return render(request, 'tienda/carrito.html', {"cart": cart})


# FUNCIÓN QUE CREA LA COMPRA PARA EL CLIENTE
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/order_form.html"

    # FUNCIÓN PARA AGREGAR DATOS DEL CLIENTE A LA COMPRA
    def form_valid(self, form):
        cart = Cart(self.request)
        if cart:
            order = form.save(commit=False)
            order.user = self.request.user
            order.is_pagado = True
            order.save()

            for item in cart:
                producto = item["producto"]
                costo = item["costo"]
                cantidad = item["cantidad"]

                # Crear un OrderItem para cada producto en el carrito
                OrderItem.objects.create(
                    orden=order,
                    item=producto,
                    costo=costo,
                    cantidad=cantidad,
                )

                # Actualizar la cantidad del producto en la base de datos
                if isinstance(producto, Producto):  # Solo si es un producto
                    Producto.objects.filter(id=producto.id).update(cantidad=F('cantidad') - cantidad)

            cart.clear()  # Limpiar el carrito después de crear la orden
            return render(self.request, 'order/ordenCreada.html', {'order': order})

        return HttpResponseRedirect(reverse("home"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context  



#FUNCIÓN QUE DEVUELVE AL USUARIO A LA PÁGINA INDICANDO PEDIDO LISTO
@login_required
def pedidoListo(request):
    
    return render(request, 'order/pedidoListo.html')


#FUNCIÓN PARA VER MIS COMPRAS Y REALIZAR SEGUIMIENTO
@login_required
def misOrdenes(request):
    ordenes = Order.objects.filter(user=request.user)
    print(ordenes)
    return render(request, 'tienda/misOrdenes.html',  {'ordenes': ordenes} )
#ATENCION CLIENTE

def atencioncliente(request):
    return render(request, 'tienda/atencioncliente.html')

#FUNCIÓN PARA OBTENER ESTADÍSTICAS DE STOCK PRODUCTOS Y PRODUCTOS MÁS VENDIDOS
def dashboard(request):
    # Obtener parámetros de fecha del cliente
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    # Convertir fechas a formato datetime
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
    else:
        # Si no se especifican fechas, usar todo el rango disponible
        fecha_inicio = None
        fecha_fin = None
    # Filtrar reservas por fecha si se proporcionan fechas válidas
    reservas = Reserva.objects.all()
    if fecha_inicio and fecha_fin:
        reservas = reservas.filter(fecha__range=(fecha_inicio, fecha_fin))


    products = Producto.objects.all() 
    product_count = products.count()

    orders = Order.objects.all()
    order_count = orders.count()

    products_sold = OrderItem.objects.values('item_id').annotate(total_quantity=Sum('cantidad')).order_by('-total_quantity')
    product_names = Item.objects.filter(id__in=[product_sold['item_id'] for product_sold in products_sold])

    products_sold_dict = {
        product_sold['item_id']: {
            'total_quantity': product_sold['total_quantity'], 
            'name': product_name.nombre
        } 
        for product_sold, product_name in zip(products_sold, product_names)
    }

    for product in products:
        if product.id in products_sold_dict:
            product.total_quantity = products_sold_dict[product.id]['total_quantity']
        else:
            product.total_quantity = 0 

    # Obtener el total de reservas, confirmadas, pendientes y eliminadas
    total_reservas = reservas.count()
    reservas_confirmadas = reservas.filter(estado='confirmado').count()
    reservas_pendientes = reservas.filter(estado='pendiente').count()
    reservas_canceladas = reservas.filter(estado='eliminado').count()

    # Tasa de cancelación (basada en el total de reservas)
    tasa_cancelacion = (reservas_canceladas / total_reservas * 100) if total_reservas > 0 else 0

    # Reservas por categoría
    reservas_por_categoria = reservas.values('servicio__categoria__nombre').annotate(total=Count('id')).order_by('servicio__categoria__nombre')

    context = {
        'products': products,
        'product_count': product_count,

        'orders': orders,
        'order_count': order_count,
        'products_sold': products_sold_dict.values(),

        # Indicadores de reservas
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_canceladas': reservas_canceladas,
        'tasa_cancelacion': tasa_cancelacion,
        'reservas_por_categoria': json.dumps(list(reservas_por_categoria)),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,   
    }
    return render(request, 'dashboard/dashboard.html', context)

def quienes_somos(request):
    return render(request, 'tienda/quienessomos.html')
