from django.urls import path
from .views import lista_categorias, agregar_categoria, lista_productos, agregar_producto, tienda, detalle_producto, \
    agregar_al_carrito, eliminar_del_carrito, ver_carrito, limpiar_carrito, historial_pedidos, editar_categoria, \
    eliminar_categoria, editar_producto, eliminar_producto
from .views import procesar_pago, pago_zelle
from django.contrib.auth.views import LogoutView
from clientes.views import admin_dashboard

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    # Categorías
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categorias/agregar/', agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    # Agregar esta línea

    # Productos
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),  # Nueva URL
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    path('tienda/', tienda, name='tienda'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),

    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/limpiar/', limpiar_carrito, name='limpiar_carrito'),

    path('pago/procesar/', procesar_pago, name='procesar_pago'),
    path('pago/zelle/', pago_zelle, name='pago_zelle'),
    path('pedidos/', historial_pedidos, name='historial_pedidos'),



]
