from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

from .models import Producto, Carrito

# Create your views here.


# lee documentos .html

# Pagina


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


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    precio_serializable = float(producto.precio)
    carrito.agregar(producto, precio_serializable)
    return redirect("productos")


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("productos")


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    precio_serializable = float(producto.precio)
    carrito.restar(producto, precio_serializable)
    return redirect("productos")


def limpiar_producto(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("productos")


def registro_cliente(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignamos al grupo cliente
            group = Group.objects.get(name="Cliente")
            user.groups.add(group)
            # Inicia sesion al usuario
            login(request, user)

            # Creamos un carrito para el usuario
            # carrrito, created = Carrito.objects.get_or_create(usuario=user)
            return redirect("inicio")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/registro_cliente.html", {"form": form})
