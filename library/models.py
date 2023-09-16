from django.db import models
from django.utils.html import format_html


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
