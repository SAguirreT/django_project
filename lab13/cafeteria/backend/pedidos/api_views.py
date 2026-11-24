from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalogo.models import Producto

from .models import Cliente, DetallePedido, Pago, Pedido


class LineaSerializer(serializers.Serializer):
    producto = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)


class PedidoSerializer(serializers.Serializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    detalles = LineaSerializer(many=True, allow_empty=False)

    def validate_detalles(self, value):
        if len({linea['producto'] for linea in value}) != len(value):
            raise serializers.ValidationError('Incluya cada producto una sola vez.')
        return value


@api_view(['POST'])
@transaction.atomic
def crear_pedido(request):
    serializer = PedidoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    pedido = Pedido.objects.create(cliente=serializer.validated_data['cliente'], total=0)
    total = Decimal('0.00')
    for linea in sorted(serializer.validated_data['detalles'], key=lambda item: item['producto']):
        producto_id = linea['producto']
        cantidad = linea['cantidad']
        disponibles = Producto.objects.filter(pk=producto_id, activo=True, stock__gte=cantidad)
        if not disponibles.update(stock=F('stock') - cantidad):
            raise serializers.ValidationError({'stock': f'Stock insuficiente o producto inactivo: {producto_id}.'})
        producto = Producto.objects.get(pk=producto_id)
        total += producto.precio * cantidad
        DetallePedido.objects.create(
            pedido=pedido, producto=producto, cantidad=cantidad, precio_unitario=producto.precio,
        )
    if total > Decimal('99999999.99'):
        raise serializers.ValidationError({'total': 'Importe fuera del rango admitido.'})
    pago = Pago.objects.create(
        pedido=pedido, importe=total, estado=Pago.Estado.APROBADO, referencia=f'SIM-{pedido.pk}',
    )
    pedido.total = total
    pedido.estado = Pedido.Estado.PAGADO
    pedido.save(update_fields=['total', 'estado'])
    return Response(
        {'id': pedido.pk, 'total': str(total), 'estado': pedido.estado, 'referencia': pago.referencia},
        status=status.HTTP_201_CREATED,
    )
