from django.db import models


class Vehicle(models.Model):
    COLORLIST = (
        ('1', 'ROJO'),
        ('2', 'AZUL'),
        ('3', 'VERDE'),
    )
    placa = models.CharField(max_length=6)
    marca = models.CharField(max_length=50)
    modelo = models.IntegerField()
    color = models.CharField(max_length=1, choices=COLORLIST)

    def __str__(self):
        return f"{self.placa} - {self.marca}"
