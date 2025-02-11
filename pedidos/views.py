from django.shortcuts import render
from clientes.models import Contacto
from productos.cart import Carrito
from django.shortcuts import redirect
from pedidos.forms import ComprobantePagoForm
from pedidos.models import Pedido, PedidoProducto
from django.contrib import messages
import logging
from django.shortcuts import render, get_object_or_404

from productos.models import Producto
from .models import Pedido
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Crear el logger
logger = logging.getLogger(__name__)


def crear_pedido(request):
    carrito = Carrito(request)

    if carrito.obtener_total() > 0:
        logger.debug("Verificando si ya existe un pedido pendiente para el usuario: %s", request.user)

        # Verificar si ya hay un pedido pendiente
        pedido, created = Pedido.objects.get_or_create(
            cliente=request.user,
            estado='pendiente',
            defaults={'total': carrito.obtener_total()}
        )

        # Si el pedido ya existía, actualizar el total
        if not created:
            pedido.total = carrito.obtener_total()
            pedido.save()
        else:
            # Si es un nuevo pedido, agregar los productos
            for producto_id, item in carrito.carrito.items():
                producto = get_object_or_404(Producto, nombre=item['nombre'])
                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    subtotal=item['subtotal']
                )

        logger.debug("Pedido %s guardado con estado pendiente", pedido.id)

        messages.success(request, "Pedido creado correctamente. ¡Ahora sube tu comprobante!")

        # Redirigir directamente al paso 2 (selección de contacto)
        return redirect('pago_paso2')

    else:
        messages.error(request, "El carrito está vacío. Agrega productos antes de continuar.")
        return redirect('ver_carrito')


def resumen_carrito(request):
    carrito = Carrito(request)

    # Si el carrito tiene productos, intentamos crear el pedido
    if carrito.obtener_total() > 0:
        return crear_pedido(request)  # Llama a la función para crear el pedido y redirigir al siguiente paso

    # Si el carrito está vacío, muestra un error
    messages.error(request, "El carrito está vacío. Agrega productos antes de continuar.")
    return redirect('ver_carrito')


def crear_o_seleccionar_contacto(request):
    contactos = Contacto.objects.filter(usuario=request.user)  # Contactos del usuario
    context = {
        'contactos': contactos
    }
    return render(request, 'pedidos/pago_paso2.html', context)


def mostrar_informacion_pago(request):
    # Datos de pago por Zelle
    informacion_pago = {
        'nombre': 'Juan Pérez',
        'correo': 'zelle@ejemplo.com',
        'banco': 'Bank of America'
    }
    context = {
        'informacion_pago': informacion_pago
    }
    return render(request, 'pedidos/pago_paso3.html', context)


def subir_comprobante_pago(request):
    if request.method == 'POST':
        form = ComprobantePagoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el último pedido pendiente del usuario
            pedido = Pedido.objects.filter(cliente=request.user, estado='pendiente').order_by('-fecha_creacion').first()

            if not pedido:
                messages.error(request, "No se encontró un pedido pendiente. Verifica que tu pedido fue creado "
                                        "correctamente.")
                return redirect('pago_paso3')  # Redirige a la información de pago

            # Guardar el comprobante de pago
            pedido.comprobante_pago = form.cleaned_data['comprobante_pago']
            pedido.estado = 'en revisión'
            pedido.save()

            messages.success(request, "Comprobante de pago subido correctamente.")
            return redirect('pago_paso5')

    else:
        form = ComprobantePagoForm()

    return render(request, 'pedidos/pago_paso4.html', {'form': form})



def confirmacion_pago(request):
    carrito = Carrito(request)
    # Limpia el carrito después de la confirmación del pedido
    carrito.limpiar()
    messages.success(request, "Tu pedido ha sido confirmado. ¡Gracias por tu compra!")
    return redirect('historial_pedidos')  # Redirige a la tienda o donde prefieras


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})


def aprobar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == "en revisión":
        pedido.estado = "aprobado"
        pedido.save()
        messages.success(request, f"El pedido {pedido.id} ha sido aprobado.")
    return redirect('gestionar_pedidos')


def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == "en revisión":
        pedido.estado = "cancelado"
        pedido.save()
        messages.success(request, f"El pedido {pedido.id} ha sido cancelado.")
    return redirect('gestionar_pedidos')
