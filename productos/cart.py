from decimal import Decimal
from django.conf import settings
from .models import Producto


class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': cantidad,
                'subtotal': str(producto.precio * cantidad),
            }
        else:
            self.carrito[producto_id]['cantidad'] += cantidad
            self.carrito[producto_id]['subtotal'] = str(
                Decimal(self.carrito[producto_id]['precio']) * self.carrito[producto_id]['cantidad']
            )
        self.guardar()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def limpiar(self):
        self.session['carrito'] = {}
        self.guardar()

    def guardar(self):
        self.session.modified = True

    def obtener_total(self):
        return sum(Decimal(item['subtotal']) for item in self.carrito.values())
