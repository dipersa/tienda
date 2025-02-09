from decimal import Decimal
from django.conf import settings
from productos.models import Producto


class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def __iter__(self):
        """
        Itera sobre los elementos en el carrito y agrega la información del producto.
        Calcula el subtotal para cada producto.
        """
        carrito = self.carrito.copy()  # Copia el carrito actual para no modificar la sesión directamente
        for producto_id, datos in carrito.items():
            try:
                producto = Producto.objects.get(id=producto_id)
                datos['producto'] = producto
                datos['subtotal'] = Decimal(datos['precio']) * datos['cantidad']  # Calcula el subtotal
            except Producto.DoesNotExist:
                datos['producto'] = None
                datos['subtotal'] = Decimal(0)  # Evita errores si el producto no existe

            yield datos  # Devuelve el diccionario completo con el subtotal incluido

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': cantidad,
            }
        else:
            self.carrito[producto_id]['cantidad'] += cantidad
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
        """
        Retorna el total acumulado del carrito.
        """
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())
