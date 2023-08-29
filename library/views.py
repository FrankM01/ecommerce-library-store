from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto  # Importamos el modelo Producto

# Create your views here.


# lee documentos .html

# Pagina


def inicio(request):
    return render(request, "paginas/inicio.html")


def nosotros(request):
    return render(request, "paginas/nosotros.html")


# Productos


def productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/index.html", {"productos": productos})
    # print(productos)


def crear_productos(request):
    return render(request, "productos/crear.html")


def editar_productos(request):
    return render(request, "productos/editar.html")
