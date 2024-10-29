from django.contrib import admin
from .models import User, Item, Reserva, Producto

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Reserva)
admin.site.register(Producto)

