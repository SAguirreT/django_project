from django.db import models


# =========================
# MODELO ZONA
# =========================

class Zona(models.Model):
    nombre_zona = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    densidad_poblacional = models.PositiveIntegerField()
    flujo_personas = models.CharField(max_length=20)
    accesibilidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_zona


# =========================
# MODELO FARMACIA
# =========================

class Farmacia(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        related_name='farmacias'
    )
    distancia_metros = models.PositiveIntegerField()
    estado = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


# =========================
# MODELO EVALUACIÓN
# =========================

NIVEL_VIABILIDAD_CHOICES = [
    ('Alta', 'Alta'),
    ('Media', 'Media'),
    ('Baja', 'Baja'),
]


class EvaluacionUbicacion(models.Model):
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        related_name='evaluaciones'
    )
    inkafarmas_cercanos = models.PositiveIntegerField()
    competidores_cercanos = models.PositiveIntegerField()
    centros_salud_cercanos = models.PositiveIntegerField()
    costo_alquiler = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    ventas_estimadas = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    nivel_viabilidad = models.CharField(
        max_length=10,
        choices=NIVEL_VIABILIDAD_CHOICES
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'Evaluación #{self.pk} - '
            f'Zona {self.zona.nombre_zona} '
            f'({self.nivel_viabilidad})'
        )