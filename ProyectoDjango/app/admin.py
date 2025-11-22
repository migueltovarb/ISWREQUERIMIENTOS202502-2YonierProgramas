
from django.contrib import admin
from django.forms import TimeInput, DateInput
from django.db import models
from .models import Voluntario, Actividad, Inscripcion, Asistencia, Certificado


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'correo', 'telefono', 'ciudad')


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'hora', 'cupos')
    # Use HTML5 input types so admin shows native pickers and accepts any valid time
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput(attrs={'type': 'time'})},
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('voluntario', 'actividad', 'fecha_inscripcion')


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'asistio', 'horas')


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('voluntario', 'actividad', 'fecha_emision')
