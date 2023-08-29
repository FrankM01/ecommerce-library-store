from django.urls import path
from . import views

from django.conf import settings  # importamos el archivo de conf de las imagenes
from django.contrib.staticfiles.urls import static  # ruta estatica q vamos a recibir

# Url propia de la app
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("nosotros", views.nosotros, name="nosotros"),
    path("productos", views.productos, name="productos"),
    path("productos/crear", views.crear_productos, name="crear"),
    path("productos/editar", views.editar_productos, name="editar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
