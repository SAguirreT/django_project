from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import serializers

from .models import Categoria, Cliente, DetalleVenta, EvaluacionUbicacion, Farmacia, Producto, Venta, Zona


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'categoria_nombre']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor que cero.')
        return value


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'documento', 'telefono', 'correo']


class FarmaciaSerializer(serializers.ModelSerializer):
    zona_nombre = serializers.CharField(source='zona.nombre_zona', read_only=True)

    class Meta:
        model = Farmacia
        fields = ['id', 'nombre', 'tipo', 'zona', 'zona_nombre', 'distancia_metros', 'estado']


    def validate_distancia_metros(self, value):
        if value <= 0:
            raise serializers.ValidationError('La distancia debe ser mayor que cero.')
        return value


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['id', 'nombre_zona', 'distrito', 'densidad_poblacional', 'flujo_personas', 'accesibilidad']


class EvaluacionUbicacionSerializer(serializers.ModelSerializer):
    # La zona se muestra anidada; este recurso se publica solo para lectura.
    zona = ZonaSerializer(read_only=True)

    class Meta:
        model = EvaluacionUbicacion
        fields = ['id', 'zona', 'inkafarmas_cercanos', 'competidores_cercanos',
                  'centros_salud_cercanos', 'costo_alquiler', 'ventas_estimadas',
                  'nivel_viabilidad', 'fecha_creacion']


class DetalleVentaReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']


class VentaReadSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    detalles = DetalleVentaReadSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'fecha', 'total', 'detalles']

class LineaVentaSerializer(serializers.Serializer):
    producto = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)


class VentaWriteSerializer(serializers.ModelSerializer):
    detalles = LineaVentaSerializer(many=True, allow_empty=False, write_only=True, required=False)
    fecha = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Venta
        fields = ['cliente', 'fecha', 'detalles']

    def validate_detalles(self, value):
        if len({linea['producto'] for linea in value}) != len(value):
            raise serializers.ValidationError('Incluya cada producto una sola vez.')
        return value

    def validate(self, attrs):
        if self.instance is not None and 'detalles' in self.initial_data:
            raise serializers.ValidationError({'detalles': 'Las líneas confirmadas son inmutables.'})
        if self.instance is None and 'detalles' not in attrs:
            raise serializers.ValidationError({'detalles': 'Agregue al menos un producto.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        detalles = validated_data.pop('detalles')
        venta = Venta.objects.create(total=0, stock_descontado=True, **validated_data)
        total = Decimal('0.00')
        for linea in sorted(detalles, key=lambda item: item['producto']):
            producto_id = linea['producto']
            cantidad = linea['cantidad']
            disponibles = Producto.objects.filter(pk=producto_id, stock__gte=cantidad, precio__gt=0)
            if not disponibles.update(stock=F('stock') - cantidad):
                raise serializers.ValidationError({'stock': f'Producto sin precio válido o stock insuficiente: {producto_id}.'})
            producto = Producto.objects.get(pk=producto_id)
            total += producto.precio * cantidad
            DetalleVenta.objects.create(
                venta=venta, producto=producto, cantidad=cantidad, precio_unitario=producto.precio,
            )
        if total > Decimal('99999999.99'):
            raise serializers.ValidationError({'total': 'Importe fuera del rango admitido.'})
        venta.total = total
        venta.save(update_fields=['total'])
        return venta

    def to_representation(self, instance):
        return VentaReadSerializer(instance, context=self.context).data
