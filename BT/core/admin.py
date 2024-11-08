from django.contrib import admin
from .models import User, Item, Reserva, Producto, Order

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Reserva)
admin.site.register(Producto)
admin.site.register(Order)

