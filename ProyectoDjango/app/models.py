from django.db import models


class Voluntario(models.Model):
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    habilidades = models.TextField(blank=True)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    lugar = models.CharField(max_length=200, blank=True, default='', verbose_name='Lugar')
    fecha = models.DateField()
    hora = models.TimeField()
    cupos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"


class Inscripcion(models.Model):
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voluntario', 'actividad')

    def __str__(self):
        return f"{self.voluntario} -> {self.actividad}"


class Asistencia(models.Model):
    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)
    horas = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Asistencia {self.inscripcion} - {self.asistio}"


class Certificado(models.Model):
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado {self.voluntario} - {self.actividad}"
