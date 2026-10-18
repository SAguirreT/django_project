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
