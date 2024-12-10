from django.template.defaultfilters import slugify
import os
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import make_aware, is_naive

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from model_utils.models import TimeStampedModel
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
from .constants import REGIONES, COMUNAS

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


#USUARIOS
class User(AbstractUser):
    CLIENTE = 'Cliente'
    ADMINISTRADOR = 'Administrador'
    
    TIPO_USUARIO = [
        (CLIENTE, 'Cliente'),
        (ADMINISTRADOR, 'Administrador'),
    ]
    
    picture = models.ImageField(default = 'users/profile_default.png', upload_to='media/users/')
    direccion = models.CharField(max_length=60, null=True, blank =True)
    region = models.CharField(max_length=200, choices=REGIONES, default=REGIONES[0][0])
    comuna = models.CharField(max_length=200, choices=COMUNAS, default=COMUNAS[0][0])
    telefono = models.CharField(max_length=9, null=True, validators=[MinLengthValidator(9)])
    fecha_nac = models.DateField(null=True)
    tipo_user = models.CharField(max_length=60, choices=TIPO_USUARIO, default=CLIENTE, null=True, blank=True )

    def save(self, *args, **kwargs):
        if self.tipo_user == self.ADMINISTRADOR:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)


# categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
# Modelo base para Producto y Servicio
class Item(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='items')
    tipo = models.CharField(max_length=50, choices=[('producto', 'Producto'), ('servicio', 'Servicio')])
    costo = models.IntegerField(default=0)
    costo2 = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='media/items/', null=True, blank=True)
    descuento = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    def save(self, *args, **kwargs):
        # Asignar el tipo automáticamente según la subclase
        if not self.tipo:
            self.tipo = 'producto' if isinstance(self, Producto) else 'servicio'
        # Calcular descuento
        if self.descuento:
            descuento_factor = (100 - self.descuento) / 100
            self.costo2 = self.costo * descuento_factor
        super().save(*args, **kwargs)


# Modelo Producto hereda de Item
class Producto(Item):
    cantidad = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'


# Modelo Servicio hereda de Item
class Servicio(Item):
    duracion = models.PositiveIntegerField(help_text="Duración en minutos", default=60)
    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

# CREACIÓN EN BD DE RESERVAS
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('pendiente', 'Pendiente'),
        ('eliminado', 'Eliminado'),
        ('enConflicto', 'En Conflicto'),
    ]
    
    cliente = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    contacto = models.CharField(max_length=13, null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='pendiente')

    @property
    def fecha_hora_inicio(self):
        return datetime.combine(self.fecha, self.hora)
    
    @property
    def fecha_hora_fin(self):
        return self.fecha_hora_inicio + timedelta(hours=1)

    def verificar_conflicto(self):
        # Verificar si hay conflicto con bloqueos activos
        bloqueos = BloqueoHorario.objects.filter(
            categoria=self.servicio.categoria,
            fecha_inicio__lte=self.fecha_hora_fin,
            fecha_fin__gte=self.fecha_hora_inicio
        )
        return bloqueos.exists()

    def save(self, *args, **kwargs):
        # Actualizar el estado automáticamente si hay conflicto
        if self.verificar_conflicto():
            self.estado = 'enConflicto'
        elif self.estado == 'enConflicto':  # Restaurar a pendiente si ya no hay conflicto
            self.estado = 'pendiente'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reserva de {self.nombre} para {self.servicio} ({self.estado}) el {self.fecha} a las {self.hora}'

#ÓRDENES
class Order(TimeStampedModel):
    ESTADO_VENTA = [
        ('En Preparación', 'En Preparación'),
        ('En Ruta', 'En Ruta'),
        ('Entregado', 'Entregado'),
    ]
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    direccion = models.CharField("Dirección", max_length=250, null = True)
    telefono = models.CharField("Teléfono", max_length=250, null = True)
    observaciones = models.CharField("Observaciones", max_length=250, blank=True)
    region = models.CharField("Región", max_length=200, choices=REGIONES, default=REGIONES[0][0])
    comuna = models.CharField("Comuna", max_length=200, choices=COMUNAS, default=COMUNAS[0][0])
    estado_venta = models.CharField("Estado Órden", max_length=200, choices=ESTADO_VENTA, default=ESTADO_VENTA[0][0])
    is_pagado = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created", )
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return 'BT{}'.format(self.id)

    def get_precio_total(self):
        total_costo = sum(item.get_precio_total() for item in self.items.all())
        return total_costo

    @property
    def description(self):
        descriptions = []
        for orderitem in self.items.all():  # accediendo a la relación de items
            description = '{} x {}'.format(orderitem.cantidad, orderitem.item.nombre)  # 'item' es el producto
            descriptions.append(description)
        return ", ".join(descriptions)

# Relación entre una orden y los ítems (producto o servicio)
class OrderItem(models.Model):
    orden = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(100)
        ]
    )
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.nombre} - {self.cantidad} unidades"

    def get_precio_total(self):
        return self.costo * self.cantidad
    

# Bloqueo de Horario
class BloqueoHorario(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='bloqueos')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    motivo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Bloqueo ({self.categoria.nombre}) del {self.fecha_inicio} al {self.fecha_fin} - {self.motivo}'


from datetime import datetime

@receiver(post_save, sender=BloqueoHorario)
def actualizar_reservas_en_conflicto(sender, instance, **kwargs):
    """
    Evalúa y actualiza reservas existentes que entren en conflicto con el nuevo bloqueo.
    También restaura el estado de las reservas que ya no están en conflicto.
    """
    bloqueo = instance

    # Convertir fechas de bloqueo a datetime (si no están en formato datetime)
    bloqueo_inicio = bloqueo.fecha_inicio if isinstance(bloqueo.fecha_inicio, datetime) else datetime.fromisoformat(bloqueo.fecha_inicio)
    bloqueo_fin = bloqueo.fecha_fin if isinstance(bloqueo.fecha_fin, datetime) else datetime.fromisoformat(bloqueo.fecha_fin)

    # Buscar todas las reservas que pertenecen a la misma categoría del bloqueo
    reservas = Reserva.objects.filter(servicio__categoria=bloqueo.categoria)

    for reserva in reservas:
        # Calcular los rangos de tiempo de la reserva
        reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
        reserva_fin = reserva_inicio + timedelta(minutes=reserva.servicio.duracion)

        # Verificar si la reserva entra en conflicto con el rango del bloqueo
        en_conflicto = (
            reserva_inicio < bloqueo_fin and
            reserva_fin > bloqueo_inicio
        )

        if en_conflicto and reserva.estado != 'enConflicto':
            # Cambiar el estado a 'enConflicto' si la reserva está afectada
            reserva.estado = 'enConflicto'
            reserva.save()
        elif not en_conflicto and reserva.estado == 'enConflicto':
            # Restaurar el estado de la reserva si ya no está en conflicto
            reserva.estado = 'pendiente'
            reserva.save()




@receiver(post_delete, sender=BloqueoHorario)
def manejar_reservas_al_eliminar_bloqueo(sender, instance, **kwargs):
    """
    Restaura el estado de las reservas afectadas cuando se elimina un bloqueo.
    """
    bloqueo = instance

    # Convertir fechas de bloqueo a datetime timezone-aware
    bloqueo_inicio = bloqueo.fecha_inicio
    bloqueo_fin = bloqueo.fecha_fin

    # Buscar todas las reservas que podrían haber estado en conflicto con este bloqueo
    reservas = Reserva.objects.filter(servicio__categoria=bloqueo.categoria)

    for reserva in reservas:
        # Calcular los rangos de tiempo de la reserva
        reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
        if is_naive(reserva_inicio):
            reserva_inicio = make_aware(reserva_inicio)

        reserva_fin = reserva_inicio + timedelta(minutes=reserva.servicio.duracion)

        # Verificar si la reserva estuvo en conflicto con el bloqueo eliminado
        estuvo_en_conflicto = (
            reserva_inicio < bloqueo_fin and
            reserva_fin > bloqueo_inicio
        )

        # Restaurar el estado de la reserva si ya no está en conflicto con ningún bloqueo
        if estuvo_en_conflicto:
            otros_bloqueos = BloqueoHorario.objects.filter(
                categoria=reserva.servicio.categoria,
                fecha_inicio__lte=reserva_fin,
                fecha_fin__gte=reserva_inicio
            )
            if not otros_bloqueos.exists() and reserva.estado == 'enConflicto':
                reserva.estado = 'pendiente'
                reserva.save()
