from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, PedidoForm
from django.contrib.auth.decorators import login_required

from .models import Carrito, DetallePedido, Pedido, Producto

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
    # carrito.guardar_carrito()

    # Agregar declaraciones print para mostrar los datos del carrito
    print("Carrito después de agregar producto:")
    for key, value in carrito.carrito.items():
        print(
            f"Producto: {value['nombre']}, Cantidad: {value['cantidad']}, Precio: {value['acumulado']}"
        )
    return redirect("productos")


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    # carrito.guardar_carrito()
    # Agregar declaraciones print para mostrar los datos del carrito
    print("Carrito después de eliminar producto:")
    for key, value in carrito.carrito.items():
        print(
            f"Producto: {value['nombre']}, Cantidad: {value['cantidad']}, Precio: {value['acumulado']}"
        )
    return redirect("productos")


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    precio_serializable = float(producto.precio)
    carrito.restar(producto, precio_serializable)
    # carrito.guardar_carrito()
    # Agregar declaraciones print para mostrar los datos del carrito
    print("Carrito después de restar producto:")
    for key, value in carrito.carrito.items():
        print(
            f"Producto: {value['nombre']}, Cantidad: {value['cantidad']}, Precio: {value['acumulado']}"
        )
    return redirect("productos")


def limpiar_producto(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("productos")


def procesar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario de  pago
            metodo_pago = form.cleaned_data["metodo_pago"]

            # Acceder al carrito del usuario
            carrito = Carrito(request)

            # Calcular el total sumando los subtotales de los productos en el carrito
            total = sum(
                item_data["acumulado"] for item_data in carrito.carrito.values()
            )
            # Crear un nuevo objeto Pedido
            pedido = Pedido(usuario=request.user, total=total, metodo_pago=metodo_pago)
            pedido.save()

            # Recorrer los productos en el carrito y crear DetallePedido para cada uno
            for item_id, item_data in carrito.carrito.items():
                producto_id = item_data["producto_id"]
                cantidad = item_data["cantidad"]
                subtotal = item_data["acumulado"]

                producto = Producto.objects.get(id=producto_id)

                detalle_pedido = DetallePedido(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal,
                )
                detalle_pedido.save()

            # Vaciar el carrito
            carrito.limpiar()

            # Redirigir a la página de confirmación de pedido con el ID del pedido
            return redirect("confirmacion_pedido", pedido.id)
    else:
        form = PedidoForm()

    # Si no es una solicitud POST, redirigir al inicio u otra página adecuada
    return render(request, "ver_carrito.html", {"form": form})


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Aquí podrías agregar lógica adicional, como enviar un correo de confirmación al usuario, etc.
    return render(request, "confirmacion_pedido.html", {"pedido": pedido})


# Funcion para hacer el registro de clientes con su respectiva asignacion de rol
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
