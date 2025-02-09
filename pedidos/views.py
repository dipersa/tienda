from django.shortcuts import render
from clientes.models import Contacto
from productos.cart import Carrito
from django.shortcuts import redirect
from pedidos.forms import ComprobantePagoForm
from pedidos.models import Pedido
from django.contrib import messages
import logging
from django.shortcuts import render, get_object_or_404
from .models import Pedido


# Crear el logger
logger = logging.getLogger(__name__)


def crear_pedido(request):
    carrito = Carrito(request)
    if carrito.obtener_total() > 0:
        logger.debug("Creando pedido para usuario: %s", request.user)
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=carrito.obtener_total(),
            estado='pendiente'
        )
        pedido.save()
        carrito.limpiar()
        logger.debug("Pedido creado con éxito, ID: %s", pedido.id)
        messages.success(request, "Pedido creado correctamente. ¡Ahora sube tu comprobante!")
        return redirect('pago_paso1')
    else:
        logger.debug("El carrito está vacío para el usuario: %s", request.user)
        messages.error(request, "El carrito está vacío. Agrega productos antes de continuar.")
        return redirect('carrito')


def resumen_carrito(request):
    carrito = Carrito(request)
    context = {
        'carrito': carrito,
        'total': carrito.obtener_total(),
    }
    return render(request, 'pedidos/pago_paso1.html', context)


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
            pedido = Pedido.objects.filter(usuario=request.user, estado='pendiente').last()
            if pedido:  # Verificar si existe un pedido pendiente
                pedido.comprobante_pago = form.cleaned_data['comprobante_pago']
                pedido.estado = 'en revisión'  # Cambiar el estado del pedido
                pedido.save()
                messages.success(request, "Comprobante de pago subido correctamente.")
                return redirect('pago_paso5')  # Redirige al paso 5
            else:
                messages.error(request, "No se encontró un pedido pendiente. Por favor, revisa tu carrito.")
                return redirect('ver_carrito')
    else:
        form = ComprobantePagoForm()

    context = {
        'form': form
    }
    return render(request, 'pedidos/pago_paso4.html', context)


def confirmacion_pago(request):
    carrito = Carrito(request)
    # Limpia el carrito después de la confirmación del pedido
    carrito.limpiar()
    messages.success(request, "Tu pedido ha sido confirmado. ¡Gracias por tu compra!")
    return redirect('historial_pedidos')  # Redirige a la tienda o donde prefieras


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})