from django.urls import path
from . import views

from django.conf import settings  # importamos el archivo de conf de las imagenes
from django.contrib.staticfiles.urls import static  # ruta estatica q vamos a recibir
from django.contrib.auth import views as auth_views


# Url propia de la app
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("nosotros", views.nosotros, name="nosotros"),
    path("productos", views.productos, name="productos"),
    path("productos/crear", views.crear_productos, name="crear"),
    path("productos/editar", views.editar_productos, name="editar"),
    path("perfil", views.perfil, name="perfil"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("agregar/<int:producto_id>/", views.agregar_producto, name="Add"),
    path("eliminar/<int:producto_id>/", views.eliminar_producto, name="Del"),
    path("restar/<int:producto_id>/", views.restar_producto, name="Sub"),
    path("limpiar/", views.limpiar_producto, name="CLS"),
    path("detalle-carrito/", views.ver_detalle_carrito, name="detalle_carrito"),
    path("procesar_pedido/", views.procesar_pedido, name="procesar_pedido"),
    path(
        "confirmacion_pedido/<int:pedido_id>/",
        views.confirmacion_pedido,
        name="confirmacion_pedido",
    ),
    path("simulated_payment/", views.simulated_payment, name="simulated_payment"),
    path("confirmacion_pago/", views.confirmacion_pago, name="confirmacion_pago"),
    path("registro/", views.registro_cliente, name="registro_cliente"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
