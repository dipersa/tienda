from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
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


class RegistroUsuarioView(View):
    def get(self, request):
        form = RegistroUsuarioForm()
        return render(request, 'clientes/registro.html', {'form': form})

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'clientes/registro.html', {'form': form})


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