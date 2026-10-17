from rest_framework import serializers

from .models import Categoria, Cliente, DetalleVenta, Farmacia, Producto, Venta


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
