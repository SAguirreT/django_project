from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from farmacia.models import (Categoria, Cliente, DetalleVenta, EvaluacionUbicacion,
                             Farmacia, Producto, Venta, Zona)


class Command(BaseCommand):
    help = 'Crea datos ficticios identificados con LAB08 sin modificar registros existentes.'

    @transaction.atomic
    def handle(self, *args, **options):
        categoria, _ = Categoria.objects.get_or_create(nombre='Salud [LAB08]',
            defaults={'descripcion': 'Categoria ficticia para pruebas REST.'})
        productos = []
        for nombre, precio, stock in [('Analgesico A', '5.50', 10), ('Analgesico B', '12.00', 6),
                                      ('Vitamina C', '8.90', 0)]:
            producto, _ = Producto.objects.get_or_create(nombre=f'{nombre} [LAB08]',
                categoria=categoria, defaults={'precio': Decimal(precio), 'stock': stock,
                                               'descripcion': 'Producto ficticio de laboratorio.'})
            productos.append(producto)
        for i, estado in enumerate(['Activa', 'Inactiva', 'ACTIVA'], start=1):
            zona, _ = Zona.objects.get_or_create(nombre_zona=f'Zona {i} [LAB08]',
                defaults={'distrito': 'Lima', 'densidad_poblacional': i * 1000,
                          'flujo_personas': 'Alto', 'accesibilidad': 'Buena'})
            Farmacia.objects.get_or_create(nombre=f'Botica {i} [LAB08]', zona=zona,
                defaults={'tipo': 'Independiente', 'estado': estado, 'distancia_metros': i * 150})
            EvaluacionUbicacion.objects.get_or_create(zona=zona,
                defaults={'inkafarmas_cercanos': i, 'competidores_cercanos': i + 1,
                          'centros_salud_cercanos': 2, 'costo_alquiler': '1500.00',
                          'ventas_estimadas': '6500.00', 'nivel_viabilidad': ['Alta', 'Media', 'Baja'][i - 1]})
            cliente, _ = Cliente.objects.get_or_create(documento=f'LAB08-{i}',
                defaults={'nombre': f'Cliente ficticio {i} [LAB08]'})
            if not Venta.objects.filter(cliente=cliente).exists():
                total = sum(p.precio * i for p in productos[:2])
                # La copia local S07 tiene estado; la versión pública puede no tenerlo.
                extra = {'estado': 'PAGADO'} if any(f.name == 'estado' for f in Venta._meta.fields) else {}
                venta = Venta.objects.create(cliente=cliente, fecha=timezone.now(), total=total, **extra)
                for producto in productos[:2]:
                    DetalleVenta.objects.create(venta=venta, producto=producto,
                                               cantidad=i, precio_unitario=producto.precio)
        self.stdout.write(self.style.SUCCESS('Datos ficticios LAB08 disponibles. Ventas de muestra, sin movimiento de stock.'))
