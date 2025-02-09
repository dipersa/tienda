from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from pedidos.models import Pedido
from productos.models import Producto, Categoria
from .models import CustomUser
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EditarPerfilForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contacto
from .forms import ContactoForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from clientes.forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from pedidos.models import Pedido


@staff_member_required
def admin_dashboard(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    pedidos = Pedido.objects.all()

    # Métricas clave
    total_ventas = sum(p.total for p in pedidos)
    total_productos = productos.count()
    total_categorias = categorias.count()
    total_pedidos = pedidos.count()

    context = {
        'productos': productos,
        'categorias': categorias,
        'total_ventas': total_ventas,
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_pedidos': total_pedidos,
    }
    return render(request, 'admin/dashboard.html', context)


def gestionar_pedidos(request):
    pedidos = Pedido.objects.filter(estado='en revisión')  # Mostrar solo pedidos en revisión
    return render(request, 'admin/gestionar_pedidos.html', {'pedidos': pedidos})


class RegistroUsuarioView(FormView):
    template_name = 'clientes/registro.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        messages.success(self.request, 'Te has registrado con éxito. Ahora puedes iniciar sesión.')
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'clientes/login.html'


@login_required
def dashboard(request):
    return render(request, 'clientes/dashboard.html', {'usuario': request.user})


@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'clientes/editar_perfil.html', {'form': form})


@login_required
def lista_contactos(request):
    contactos = request.user.contactos.all()
    return render(request, 'clientes/lista_contactos.html', {'contactos': contactos})


@login_required
def agregar_contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.usuario = request.user
            contacto.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm()

    return render(request, 'clientes/agregar_contacto.html', {'form': form})


@login_required
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id, usuario=request.user)

    if request.method == "POST":
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)

    return render(request, 'clientes/editar_contacto.html', {'form': form})


@login_required
def eliminar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id, usuario=request.user)
    contacto.delete()
    return redirect('lista_contactos')
