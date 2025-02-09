from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas existentes...
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('pago/paso1/', views.resumen_carrito, name='resumen_carrito'),
    path('pago/paso2/', views.crear_o_seleccionar_contacto, name='pago_paso2'),
    path('pago/paso3/', views.mostrar_informacion_pago, name='pago_paso3'),
    path('pago/paso4/', views.subir_comprobante_pago, name='pago_paso4'),
    path('pago/paso5/', views.confirmacion_pago, name='pago_paso5'),
    path('detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    path('detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('aprobar/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    path('cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
]
