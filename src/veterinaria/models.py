from django.db import models


class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100, blank=True)
    edad = models.IntegerField()

    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.CASCADE,
        related_name='mascotas'
    )

    def __str__(self):
        return self.nombre


class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Cita(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Cita {self.id} - {self.fecha}"


class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre