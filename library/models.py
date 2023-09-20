from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User


# Create your models here.
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    imagen = models.ImageField(upload_to="imagenes/", verbose_name="Imagen", null=True)
    marca = models.CharField(max_length=100, verbose_name="Marca")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(verbose_name="Stock")

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

    def calcular_total(self):
        total = sum(
            item.producto.precio * item.cantidad for item in self.carritoitem_set.all()
        )
        return total


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
