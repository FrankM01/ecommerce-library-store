from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, CarritoItem  # Importamos el modelo Producto

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


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidad = int(request.POST.get("cantidad", 1))
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user, estado="activo"
    )

    # Verifica si el producto ya está en el carrito y, en ese caso, actualiza la cantidad
    if CarritoItem.objects.filter(carrito=carrito, producto=producto).exists():
        carrito_item = CarritoItem.objects.get(carrito=carrito, producto=producto)
        carrito_item.cantidad += cantidad
        carrito_item.save()
    else:
        carrito_item = CarritoItem(
            carrito=carrito, producto=producto, cantidad=cantidad
        )
        carrito_item.save()

    return redirect("ver_carrito")


def eliminar_del_carrito(request, carrito_item_id):
    carrito_item = get_object_or_404(CarritoItem, pk=carrito_item_id)
    if carrito_item.carrito.usuario == request.user:
        carrito_item.delete()
    return redirect("ver_carrito")


def ver_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user, estado="activo")
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})
