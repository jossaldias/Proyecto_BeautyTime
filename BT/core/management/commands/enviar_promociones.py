from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from core.models import Reserva

class Command(BaseCommand):
    help = 'Envia correos promocionales para reservas pasadas'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando envío de correos promocionales..."))

        # Obtener la fecha actual en la zona horaria local
        fecha_actual = timezone.localtime(timezone.now()).date()

        # Definir las categorías y los tiempos en semanas para enviar los correos
        promociones = {
            "uñas": 2,  # 2 semanas para categoría "uñas"
            "corporal": 3,  # 3 semanas para categoría "corporal",
        }

        # Servicios específicos dentro de la categoría "peluquería" con sus tiempos
        peluqueria_servicios = {
            "Baño de Color": 4,
            "Tinturado": 4,
            "Balayage": 4,
            "Corte de Cabello": 4,
            "Highlights": 3,
            "Brushing": 2,
        }

        # Procesar categorías con tiempos generales
        for categoria, semanas in promociones.items():
            # Calcular la fecha límite para enviar la promoción
            fecha_promocion = fecha_actual - timedelta(weeks=semanas)

            # Filtrar reservas por categoría y por la fecha exacta
            reservas = Reserva.objects.filter(
                servicio__categoria__nombre=categoria,
                fecha=fecha_promocion,
            )

            self.stdout.write(f"Categoría '{categoria}': Reservas encontradas para promoción: {reservas.count()}")

            # Enviar un correo promocional a cada cliente
            for reserva in reservas:
                self._enviar_correo_promocional(reserva, categoria)

        # Procesar servicios específicos dentro de la categoría "peluquería"
        for servicio, semanas in peluqueria_servicios.items():
            # Calcular la fecha límite para enviar la promoción
            fecha_promocion = fecha_actual - timedelta(weeks=semanas)

            # Filtrar reservas por servicio específico y por la fecha exacta
            reservas = Reserva.objects.filter(
                servicio__nombre=servicio,
                servicio__categoria__nombre="peluquería",
                fecha=fecha_promocion,
            )

            self.stdout.write(f"Servicio '{servicio}' (Peluquería): Reservas encontradas para promoción: {reservas.count()}")

            # Enviar un correo promocional a cada cliente
            for reserva in reservas:
                self._enviar_correo_promocional(reserva, servicio)

        self.stdout.write(self.style.SUCCESS("Envío de correos promocionales completado."))

    def _enviar_correo_promocional(self, reserva, categoria_servicio):
        """
        Envía un correo promocional para la reserva y categoría o servicio especificado.
        """
        self.stdout.write(f"Enviando correo promocional a {reserva.email} para '{categoria_servicio}'")

        # Asunto del correo
        asunto = f"¡Esperamos que hayas disfrutado tu última reserva de {categoria_servicio}!"

        # Enlace promocional
        promocion_url = "http://127.0.0.1:8000/paginas/servicios"
        link_amigable = f'<a href="{promocion_url}">Reservar ahora</a>'

        # Mensaje en formato HTML
        mensaje_html = (
            f'Estimado/a {reserva.nombre},<br><br>'
            f'¿Qué tal han estado tus resultados desde tu última reserva en la categoría/servicio <strong>{categoria_servicio}</strong>?<br>'
            f'Nos encantaría que nos visites nuevamente y aproveches nuestros servicios.<br><br>'
            f'¡Reserva ahora haciendo clic en este enlace: {link_amigable}!<br><br>'
            f'Te esperamos en Av. Las Perdices 2900 Local 33, Peñalolén, Región Metropolitana.'
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
