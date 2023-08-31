from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Producto  # Importamos el modelo Producto

# Create your views here.


# lee documentos .html

# Pagina


@login_required
def inicio(request):
    username = request.user.username
    return render(request, "paginas/inicio.html", {"username": username})


def nosotros(request):
    return render(request, "paginas/nosotros.html")


def perfil(request):
    return render(request, "paginas/perfil.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("inicio")  # Cambia 'inicio' al nombre de tu vista de inicio
        else:
            # Manejar el caso cuando las credenciales no son válidas
            pass
    return render(request, "login.html")


# Productos


def productos(request):
    productos = Producto.objects.all().order_by("nombre", "stock")
    return render(request, "productos/index.html", {"productos": productos})
    # print(productos)


def crear_productos(request):
    return render(request, "productos/crear.html")


def editar_productos(request):
    return render(request, "productos/editar.html")
