from django.urls import path
from .views import RegistroUsuarioView, lista_contactos, editar_contacto, eliminar_contacto, agregar_contacto, \
    admin_dashboard
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from .views import dashboard, editar_perfil
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),

    # Recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='clientes/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='clientes/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='clientes/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='clientes/password_reset_complete.html'),
         name='password_reset_complete'),

    path('dashboard/', dashboard, name='dashboard'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),

    path('contactos/', lista_contactos, name='lista_contactos'),
    path('contactos/agregar/', agregar_contacto, name='agregar_contacto'),
    path('contactos/editar/<int:contacto_id>/', editar_contacto, name='editar_contacto'),
    path('contactos/eliminar/<int:contacto_id>/', eliminar_contacto, name='eliminar_contacto'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),

]
