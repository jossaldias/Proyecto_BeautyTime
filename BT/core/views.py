import os
import requests
import time
import string


from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
import json

from django.db.models import Q, F, Sum
from .models import *
from .forms import *
from .cart import Cart


from .utils import render_to_pdf
from django.views.generic import View, CreateView 
from django.core.mail import send_mail

from datetime import timedelta, datetime
from django.contrib.auth.models import AnonymousUser


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
    servicios = Producto.objects.filter(
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
    productos = Producto.objects.filter(
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
    item = get_object_or_404(Producto, iditem=id)
    if item.tipo != tipo:
        return render(request, '404.html')  
    context = {
        'item': item,
        'tipo': tipo
    }
    return render(request, 'tienda/verDetalle.html', context)

class verInventario(View):

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        
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
    productos = Producto.objects.all()
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

            # Verificar si ya hay una reserva para la misma **categoría** en la misma hora
            reserva_existente = Reserva.objects.filter(
                servicio__categoria=categoria,
                fecha=fecha,
                hora__lt=(fecha_hora_fin.time()),  # Compara con la hora final
                hora__gte=hora  # Compara con la hora de inicio
            )

            if reserva_existente.exists():
                form.add_error(None, f'Ya existe una reserva para esta categoría ({categoria.nombre}) en el horario seleccionado.')
                return render(request, 'agenda/reservar_cita.html', {'form': form, 'reservas': reservas, 'usuario_autenticado': usuario_autenticado})

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
    asunto = 'Confirmación de cita en Capricho Divino'
    mensaje = f'Estimado/a {nombre},\n\n' \
              f'¡Su cita para el servicio {categoria.nombre} - {servicio.nombre} ha sido agendada con éxito!.\n' \
              f'Fecha y hora: {fecha_hora_inicio.strftime("%Y-%m-%d %H:%M")}\n' \
              f'Dirección: Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana.\n\n'\
              f'Si tienes alguna consulta, no dudes en contactarnos.\n\n' \
              f'Saludos,\nCapricho Divino'
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


# FUNCIÓN PARA OBTENER RESERVAS (reservar_cita.html)
def obtener_reservas(request):
    categoria_id = request.GET.get('categoria')
    user = request.user
    contexto = request.GET.get('contexto', 'calendario')  # Se agrega 'calendario' por defecto

    # Si se proporciona una categoría, filtrar las reservas por los servicios de esa categoría
    if categoria_id:
        reservas = Reserva.objects.filter(servicio__categoria_id=categoria_id)  # Filtrar por la categoría del servicio
    else:
        reservas = Reserva.objects.all()  # Devuelve todas las reservas si no se filtra por categoría

    # Si el usuario es cliente y el contexto es 'calendario', mostramos solo sus citas
    if contexto == 'calendario' and user.tipo_user != 'admin':
        reservas = reservas.filter(cliente=user)

    reservas_data = [{
        'id': reserva.id,
        'categoria': reserva.servicio.categoria.nombre,  # Asegúrate de usar el nombre de la categoría
        'nombre': reserva.nombre,
        'email': reserva.email,  # Agregando el email
        'contacto': reserva.contacto,  # Agregando el número de contacto
        'servicio': reserva.servicio.nombre,  # Añadir el nombre del servicio
        'hora_inicio': reserva.hora.strftime("%H:%M"),  # Hora de inicio correctamente formateada
        'hora_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).strftime("%H:%M"),  # Hora fin
        'fecha_inicio': datetime.combine(reserva.fecha, reserva.hora).isoformat(),
        'fecha_fin': (datetime.combine(reserva.fecha, reserva.hora) + timedelta(hours=1)).isoformat(),
        'confirmado': reserva.confirmado
    } for reserva in reservas]

    return JsonResponse({'reservas': reservas_data})

# Eliminar cita
#@login_required
def eliminar_cita(request, id):
    if request.method == 'POST':
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
                    'Actualización de su cita en Capricho Divino',
                    f'Estimado/a {reserva.nombre}, su cita ha sido modificada. Los detalles actualizados son:\n\n'
                    f'Categoría: {categoria.nombre}\n'
                    f'Servicio: {servicio.nombre}\n'
                    f'Fecha: {reserva.fecha}\n'
                    f'Hora: {reserva.hora}\n'
                    f'Dirección: Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana\n'
                    f'\n\nGracias por confiar en Capricho Divino.',
                    'beautytimeagenda@gmail.com',
                    [reserva.email],
                    fail_silently=False,
                )

            return JsonResponse({'success': True})
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def obtener_categorias(request):
    categorias = CategoriaServicio.objects.all()
    categorias_data = [{'id': categoria.id, 'nombre': categoria.nombre} for categoria in categorias]
    return JsonResponse({'categorias': categorias_data})

def obtener_servicios(request):
    categoria_id = request.GET.get('categoria_id')
    
    if categoria_id:
        servicios = Servicio.objects.filter(categoria_id=categoria_id)
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
        if user.tipo_user != 'admin' and reserva.cliente != user:
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
            'confirmado': reserva.confirmado,
            'es_admin': user.tipo_user == 'admin'  # Determina si es administrador para la lógica del frontend
        }

        return JsonResponse(reserva_data)

    except Reserva.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reserva no encontrada.'}, status=404)

# Confirmar reservas ya sea por correo desde el cliente o por whatsapp desde el admin.
def confirmar_reserva(request, reserva_id):
    # Obtener la reserva por ID
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        # Si es un POST, se confirma desde el admin que se contactó por whatsapp
        reserva.confirmado = True
        reserva.save()
        return JsonResponse({'success': True})

    elif request.method == 'GET':
        # Si es un GET, se confirma desde el cliente por correo
        if 'accion' in request.GET and request.GET['accion'] == 'confirmar':
            reserva.confirmado = True
            reserva.save()
            return render(request, 'agenda/confirmacion_exitosa.html', {'reserva': reserva})
        else:
            return render(request, 'agenda/confirmacion_fallida.html')
    
    # Si el método no es GET o POST, devolver un error
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

#CARRITO
from django.shortcuts import render

def carrito(request):
    return render(request, 'tienda/carrito.html')  

#FUNCIÓN PARA AGREGAR UN PRODUCTO MÁS AL CARRITO CON BOTÓN +
def cart_add(request, producto_id):

  cart = Cart(request)
  producto = get_object_or_404(Producto, id=producto_id)

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
  return redirect("carritoCompras")

#FUNCIÓN QUE MUESTRA EL DETALLE DE LA COMPRA 
def cart_detalle(request):
  cart = Cart(request)
  return render(request, 'tienda/carrito.html', {"cart": cart})

#ATENCION CLIENTE

def atencioncliente(request):
    return render(request, 'tienda/atencioncliente.html')

