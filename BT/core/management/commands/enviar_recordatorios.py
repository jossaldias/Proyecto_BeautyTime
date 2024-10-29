from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from core.models import Reserva

class Command(BaseCommand):
    help = 'Envia recordatorios de reservas'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando envío de recordatorios..."))

        # Obtener la fecha y hora actual en la zona horaria local
        ahora_local = timezone.localtime(timezone.now())

        # Obtener la fecha de mañana en la zona horaria local
        manana_local = ahora_local + timedelta(days=1)
        self.stdout.write(f"Fecha de mañana (local): {manana_local.date()}")

        # Filtrar reservas que están programadas para mañana (zona horaria local) y que no han sido confirmadas
        reservas = Reserva.objects.filter(fecha=manana_local.date(), confirmado=False)
        self.stdout.write(f"Reservas encontradas: {reservas.count()}")

        # Enviar un correo a cada cliente con una reserva para mañana
        for reserva in reservas:
            self.stdout.write(f"Enviando correo a {reserva.email}")

            # Obtener la categoría y el servicio
            servicio = reserva.servicio
            categoria = servicio.categoria.nombre

            # Formatear la hora sin los segundos
            hora_formateada = reserva.hora.strftime("%H:%M")

            # Asunto del correo
            asunto = f'Recordatorio Reserva en Capricho Divino'

            # Enlace de confirmación local para pruebas
            confirmacion_url = f'http://localhost:8000/confirmar_reserva/{reserva.id}?accion=confirmar'
            link_amigable = f'<a href="{confirmacion_url}">Confirmar asistencia</a>'

            # Mensaje en formato HTML
            mensaje_html = (
                f'Estimado/a {reserva.nombre},<br><br>'
                f'Este es un recordatorio de su reserva con nosotros para el servicio <strong>{categoria} - {servicio.nombre}</strong> '
                f'agendada para mañana a las {hora_formateada}.<br>'
                f'En Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana.<br><br>'
                f'Por favor, confirme su asistencia haciendo clic en el siguiente enlace: {link_amigable}.'
            )

            # Enviar el correo en formato HTML
            send_mail(
                asunto,
                '',  # Deja el cuerpo de texto plano vacío
                'beautytimeagenda@gmail.com',
                [reserva.email],
                fail_silently=False,
                html_message=mensaje_html,  # Contenido HTML del correo
            )
            self.stdout.write(self.style.SUCCESS(f"Correo enviado a {reserva.email}"))
