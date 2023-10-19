from django.core.validators import FileExtensionValidator
from django.utils.html import format_html
from django.contrib.auth.models import User, Group
from django.db import models
from .validators import *

# Var globales

# Creacion de clientes en la administracion de Grupos de Django.
client_group, created = Group.objects.get_or_create(name="Cliente")

User.add_to_class("age", models.PositiveIntegerField(default=1))
User.add_to_class("phone_number", models.CharField(max_length=9, default=""))


# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Categoria",
        validators=[validate_cate_length, validate_cate_letters_only],
        null=True,
        blank=True,
    )
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def clean(self):
        existing_categories = Categoria.objects.filter(nombre=self.nombre)
        if self.pk:
            existing_categories = existing_categories.exclude(pk=self.pk)
        if existing_categories.exists():
            raise ValidationError("Ya existe una categoria con este nombre.")


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=51,
        verbose_name="Nombre",
        validators=[validate_nombre_length, validate_nombre],
    )
    imagen = models.ImageField(
        upload_to=custom_upload_to,
        verbose_name="Imagen",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_image_size,
        ],
        null=True,
    )
    marca = models.CharField(
        max_length=100,
        verbose_name="Marca",
        validators=[validate_marca_length, validate_marca_letters_only],
        null=True,
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio",
        validators=[validate_precio],
        null=True,
    )
    stock = models.PositiveIntegerField(
        verbose_name="Stock",
        validators=[validate_stock_range, validate_stock_positive],
        null=True,
    )

    def __str__(self):
        fila = (
            "Nombre: "
            + self.nombre
            + " - "
            + "Marca: "
            + self.marca
            + " - "
            + "Precio: "
            + str(self.precio)
            + " - "
            + "Stock: "
            + str(self.stock)
        )
        return fila

    # Borra imagenes de nuestra tabla
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

    def estado_stock(self):
        if self.stock >= 10:
            return format_html(
                '<span style="color: blue;">{0}</span>'.format(self.stock)
            )
        else:
            return format_html(
                '<span style="color: red;">{0}</span>'.format(self.stock)
            )


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoItem")

    # Asegura que cada usuario tenga un carrito al iniciar sesion
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    # Metodos de agregar, guardar, eliminar, restar y limpiar

    def agregar(self, producto, precio):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "acumulado": precio,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto, precio):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= precio
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def obtener_carrito(self):
        return self.carrito


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)


class PaymentInfo(models.Model):
    pedido = models.OneToOneField("Pedido", on_delete=models.CASCADE, null=True)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_vencimiento = models.CharField(max_length=5)
    codigo_seguridad = models.CharField(max_length=3)
    metodo_pago = models.CharField(max_length=16)


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="DetallePedido")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default="pendiente")
    payment_info = models.OneToOneField(
        PaymentInfo,
        on_delete=models.CASCADE,
        related_name="pedido_payment_info",
        default=None,
        null=True,
    )


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
