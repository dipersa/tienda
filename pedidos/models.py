from django.db import models
from django.contrib.auth import get_user_model

from clientes.models import Contacto
from productos.models import Producto

User = get_user_model()


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')],
                              default='pendiente')
    comprobante_pago = models.ImageField(upload_to='comprobantes/', blank=True, null=True)
    contacto = models.ForeignKey(Contacto, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.email} - {self.estado}"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Pedido {self.pedido.id}"
