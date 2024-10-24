import copy
from decimal import Decimal
from django.conf import settings
from .models import Producto
from .forms import ProviderAddProductoForm


class Provider:

  def __init__(self, request):
    if request.session.get(settings.PROVIDER_SESSION_ID) is None:
      request.session[settings.PROVIDER_SESSION_ID] = {}

    self.provider = request.session[settings.PROVIDER_SESSION_ID]
    self.num_products = len(self.provider.items())
    self.session = request.session

  def __iter__(self):
    provider = copy.deepcopy(self.provider)
    productos = Producto.objects.filter(id__in=provider)
    for producto in productos:
      provider[str(producto.id)]["producto"] = producto

    for item in provider.values():
      item["costo"] = Decimal(item["costo"])
      item["precio_total"] = item["cantidad"] * item["costo"]
      item["update_cantidad_form"] = ProviderAddProductoForm(
        initial={
          "cantidad": item["cantidad"],
          "override": True
        }
      )
      yield item

  def __len__(self):
    return sum(item["cantidad"] for item in self.provider.values())

  def add(self, producto, cantidad=1, override_cantidad=False):
    producto_id = str(producto.id)

    if producto_id not in self.provider:
      self.provider[producto_id] = {
        "cantidad": 0,
        "costo": str(producto.costo),
      }

    if override_cantidad:
      self.provider[producto_id]["cantidad"] = cantidad
    else:
      self.provider[producto_id]["cantidad"] += cantidad
    self.provider[producto_id]["cantidad"] = min(5000, self.provider[producto_id]["cantidad"])
    self.save()

  def remove(self, producto):
    producto_id = str(producto.id)

    if producto_id in self.provider:
      del self.provider[producto_id]
      self.save()

  def get_precio_total(self):
    return sum(Decimal(item["costo"]) * item["cantidad"] for item in self.provider.values())

  def clear(self):
    del self.session[settings.PROVIDER_SESSION_ID]
    self.save()

  def save(self):
    self.session.modified = True
