import uuid
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, SimulatedPaymentForm
from django.contrib.auth.decorators import login_required

from .models import Carrito, DetallePedido, PaymentInfo, Pedido, Producto

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


def ver_detalle_carrito(request):
    # Acceder al carrito del usuario
    carrito = Carrito(request)

    # Obtener los elementos del carrito
    elementos_carrito = carrito.obtener_carrito()

    for elemento_id, elemento_info in elementos_carrito.items():
        elemento_info["subtotal"] = (
            elemento_info["cantidad"] * elemento_info["acumulado"]
        )

    return render(
        request, "detalle_carrito.html", {"elementos_carrito": elementos_carrito}
    )


def procesar_pedido(request):
    if request.method == "POST":
        # Acceder al carrito del usuario
        carrito = Carrito(request)

        # Calcular el total sumando los subtotales de los productos en el carrito
        total = sum(item_data["acumulado"] for item_data in carrito.carrito.values())

        # Recuperar el ID de PaymentInfo de la sesión
        payment_info_id = request.session.get("payment_info_id")

        if payment_info_id:
            # Crear un objeto Pedido y asignarle el PaymentInfo asociado
            pedido = Pedido(
                usuario=request.user, total=total, payment_info_id=payment_info_id
            )
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
                # Actualizar el stock del producto
                producto.stock -= cantidad
                producto.save()

            # Vaciar el carrito
            carrito.limpiar()

            # Redirigir a la página de confirmación de pedido con el ID del pedido
            return redirect("confirmacion_pedido", pedido.id)

    # Si no es una solicitud POST o no hay payment_info_id en la sesión, redirigir al inicio u otra página adecuada
    return render(request, "ver_carrito.html")


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    payment_info = pedido.payment_info
    # Aquí podrías agregar lógica adicional, como enviar un correo de confirmación al usuario, etc.
    return render(
        request,
        "confirmacion_pedido.html",
        {"pedido": pedido, "payment_info": payment_info},
    )


def simulated_payment(request):
    if request.method == "POST":
        form = SimulatedPaymentForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario simulado
            card_number = form.cleaned_data["card_number"]
            expiration_date = form.cleaned_data["expiration_date"]
            security_code = form.cleaned_data["security_code"]
            metodo_pago = form.cleaned_data["metodo_pago"]

            # Valida que los campos cumplan con tus criterios
            if (
                card_number == "12345678910"
                and expiration_date == "12/25"
                and security_code == "123"
            ):
                # Crea un objeto PaymentInfo y guárdalo en la base de datos
                payment_info = PaymentInfo(
                    numero_tarjeta=card_number,
                    fecha_vencimiento=expiration_date,
                    codigo_seguridad=security_code,
                    metodo_pago=metodo_pago,
                )
                payment_info.save()

                # Almacena el ID de PaymentInfo en la sesión
                request.session["payment_info_id"] = payment_info.id
                # Luego redirige a la vista de confirmación del pedido
                return redirect("confirmacion_pago")
            else:
                form.add_error(None, "Los datos de la tarjeta son inválidos.")
        else:
            form.add_error(None, "El formulario no es válido. Revise los campos.")
    else:
        form = SimulatedPaymentForm()

    return render(request, "simulated_payment.html", {"form": form})


def confirmacion_pago(request):
    # Obtener y mostrar los datos del pago simulado
    # Puedes acceder a los datos guardados en el paso anterior o simplemente mostrar datos simulados.
    return render(request, "confirmacion_pago.html")


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
