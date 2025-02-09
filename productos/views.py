from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Producto, Categoria
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .cart import Carrito

from pedidos.models import Pedido, PedidoProducto

import stripe
from django.conf import settings
from django.shortcuts import render, redirect

from .cart import Carrito
from django.contrib.auth.views import LogoutView

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from clientes.forms import RegistroUsuarioForm


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})


@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'productos/agregar_categoria.html', {'form': form})


@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/editar_categoria.html', {'form': form})


@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'productos/eliminar_categoria.html', {'categoria': categoria})


@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})


@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/agregar_producto.html', {'form': form})


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})


def tienda(request):
    categoria_id = request.GET.get('categoria', None)
    productos = Producto.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    return render(request, 'productos/tienda.html', {'productos': productos, 'categorias': categorias})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'productos/carrito.html', {'carrito': carrito})


def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))  # Obtener cantidad del formulario
    carrito.agregar(producto, cantidad)
    return redirect('ver_carrito')


def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect('ver_carrito')


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('ver_carrito')


def procesar_pago(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # Crear un PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Stripe maneja centavos
            currency='usd',
            metadata={'user_id': request.user.id},
        )
        return render(request, 'pagos/confirmacion_pago.html', {'client_secret': intent.client_secret, 'total': total})

    return render(request, 'pagos/procesar_pago.html', {'total': total})


def pago_zelle(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()
    return render(request, 'pagos/pago_zelle.html', {'total': total})


def confirmar_pago(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()

    # Crear el pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        estado='completado'
    )

    # Guardar los productos comprados
    for item in carrito.carrito.values():
        producto = Producto.objects.get(nombre=item['nombre'])
        PedidoProducto.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            subtotal=item['subtotal']
        )

    # Limpiar carrito después del pago
    carrito.limpiar()

    return render(request, 'pagos/pedido_confirmado.html', {'pedido': pedido})


@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'clientes/historial_pedidos.html', {'pedidos': pedidos})
