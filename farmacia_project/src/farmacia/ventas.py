from django.db import transaction
from django.db.models import F

from .models import Producto, Venta


@transaction.atomic
def eliminar_venta(venta_id):
    venta = Venta.objects.select_for_update().get(pk=venta_id)
    if venta.stock_descontado:
        for detalle in venta.detalles.order_by('producto_id'):
            Producto.objects.filter(pk=detalle.producto_id).update(stock=F('stock') + detalle.cantidad)
    venta.delete()
