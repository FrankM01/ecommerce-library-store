from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext as _
from django.utils.html import format_html
from django.contrib.auth.models import User, Group

# Var globales

# Creacion de clientes en la administracion de Grupos de Django.
client_group, created = Group.objects.get_or_create(name="Cliente")

User.add_to_class("age", models.PositiveIntegerField(default=1))
User.add_to_class("phone_number", models.CharField(max_length=9))


# Functions
def validate_nombre_length(value):
    if not 4 <= len(value) <= 50:
        raise ValidationError(
            _("El nombre debe tener entre 4 y 50 caracteres."),
            code="invalid_nombre_length",
        )


def validate_marca_length(value):
    if not 3 <= len(value) <= 30:
        raise ValidationError(
            _("La marca debe tener entre 3 y 30 caracteres."),
            code="invalid_nombre_length",
        )


def validate_cate_length(value):
    if not 3 <= len(value) <= 30:
        raise ValidationError(
            _("La categoria debe tener entre 3 y 30 caracteres."),
            code="invalid_nombre_length",
        )


def validate_nombre(value):
    if not value.strip():
        raise ValidationError(
            _("El nombre no puede estar en blanco."), code="invalid_nombre"
        )


def custom_upload_to(instance, filename):
    # Genera un nombre de archivo único o un subdirectorio basado en el producto o ID del producto
    return f"productos/{instance.id}/{filename}"


def validate_image_size(value):
    # Obtiene el tamaño del archivo en bytes
    file_size = value.size

    # Establece el tamaño máximo permitido en bytes (en este caso, 5 MB)
    max_size = 5 * 1024 * 1024  # 5 MB en bytes

    if file_size > max_size:
        raise ValidationError(
            _("El tamaño del archivo no debe superar los 5 MB."),
            code="invalid_image_size",
        )


def validate_marca_letters_only(value):
    # Verifica si el valor contiene solo letras (sin caracteres especiales ni números)
    if not value.isalpha():
        raise ValidationError(
            _("La marca no debe contener caracteres especiales ni números."),
            code="invalid_marca_letters_only",
        )


def validate_cate_letters_only(value):
    # Verifica si el valor contiene solo letras (sin caracteres especiales ni números)
    if not value.isalpha():
        raise ValidationError(
            _("La marca no debe contener caracteres especiales ni números."),
            code="invalid_marca_letters_only",
        )


def validate_precio(value):
    # Verifica si el valor contiene solo dígitos y un solo punto decimal
    value_str = str(value)
    if not value_str.replace(".", "", 1).isdigit():
        raise ValidationError(
            _("El precio debe ser un número válido con hasta 2 decimales."),
            code="invalid_precio",
        )


def validate_stock_range(value):
    # Verifica si el valor está dentro del rango permitido (0 a 1000)
    if value is None or not (0 <= value <= 9999):
        raise ValidationError(
            _("El stock debe ser un número entero entre 0 y 9999."),
            code="invalid_stock_range",
        )


def validate_stock_positive(value):
    # Verifica si el valor es un número positivo
    if value is None or value < 0:
        raise ValidationError(
            _("El stock debe ser un número entero positivo."),
            code="invalid_stock_positive",
        )


# Create your models here.
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
    categoria = models.CharField(
        max_length=100,
        verbose_name="Categoria",
        validators=[validate_cate_length, validate_cate_letters_only],
        null=True,
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoItem")
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=100)

    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

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


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
