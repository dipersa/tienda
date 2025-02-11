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
                'cantidad': cantidad,
                'precio': str(producto.precio),
                'subtotal': str(float(producto.precio) * cantidad),
            }
        else:
            self.carrito[producto_id]['cantidad'] += cantidad
            self.carrito[producto_id]['subtotal'] = str(
                float(self.carrito[producto_id]['precio']) * self.carrito[producto_id]['cantidad']
            )
        self.guardar()

    def actualizar(self, producto, cantidad):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] = cantidad
            self.carrito[producto_id]['subtotal'] = str(
                float(self.carrito[producto_id]['precio']) * cantidad
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
        return sum(
            float(item.get('subtotal', 0)) for item in self.carrito.values()
        )


