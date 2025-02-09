from django.db import models
from django.contrib.auth import get_user_model

from clientes.models import Contacto
from productos.models import Producto
from django.conf import settings

User = get_user_model()


class Pedido(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('en revisión', 'En Revisión'),
            ('pendiente', 'Pendiente'),
            ('aprobado', 'Aprobado'),
            ('cancelado', 'Cancelado')
        ]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Pedido {self.pedido.id}"
