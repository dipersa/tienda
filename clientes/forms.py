from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView
from django.db import models
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from .models import CustomUser, Contacto

from django import forms
from .models import CustomUser


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border rounded w-full p-3'}),
                               label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border rounded w-full p-3'}),
                                         label="Confirmar Contraseña")

    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellidos', 'email', 'celular', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            self.add_error("confirmar_password", "Las contraseñas no coinciden.")


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellidos', 'celular', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'apellidos', 'celular', 'direccion']
