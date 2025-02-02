from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre', 'apellidos']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Contacto(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contactos")
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    celular = models.CharField(max_length=15)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.celular}"

