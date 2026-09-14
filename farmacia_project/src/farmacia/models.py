from django.db import models


class Zona(models.Model):
    nombre_zona = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    densidad_poblacional = models.PositiveIntegerField()
    flujo_personas = models.CharField(max_length=20)
    accesibilidad = models.CharField(max_length=20)

    def __str__(self): return self.nombre_zona


class Farmacia(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='farmacias')
    distancia_metros = models.PositiveIntegerField()
    estado = models.CharField(max_length=20)

    def __str__(self): return self.nombre


NIVEL_VIABILIDAD_CHOICES = [('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')]


class EvaluacionUbicacion(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='evaluaciones')
    inkafarmas_cercanos = models.PositiveIntegerField()
    competidores_cercanos = models.PositiveIntegerField()
    centros_salud_cercanos = models.PositiveIntegerField()
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    ventas_estimadas = models.DecimalField(max_digits=10, decimal_places=2)
    nivel_viabilidad = models.CharField(max_length=10, choices=NIVEL_VIABILIDAD_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f'Evaluación #{self.pk} - Zona {self.zona.nombre_zona} ({self.nivel_viabilidad})'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    class Meta: ordering = ['nombre']
    def __str__(self): return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    class Meta: ordering = ['nombre']
    def __str__(self): return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200, blank=True)
    class Meta: ordering = ['nombre']
    def __str__(self): return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    documento = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    class Meta: ordering = ['nombre']
    def __str__(self): return f'{self.nombre} ({self.documento})'


class PerfilCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='perfil')
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    def __str__(self): return f'Perfil de {self.cliente.nombre}'


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    productos = models.ManyToManyField(Producto, through='DetalleVenta', related_name='ventas')
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta: ordering = ['-fecha']
    def __str__(self): return f'Venta #{self.pk} - {self.cliente}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_venta')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        ordering = ['venta', 'pk']
        constraints = [models.UniqueConstraint(fields=['venta', 'producto'], name='detalle_venta_producto_unico')]
    @property
    def subtotal(self): return self.cantidad * self.precio_unitario
    def __str__(self): return f'{self.venta} - {self.producto}'
