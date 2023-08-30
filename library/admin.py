from django.contrib import admin
from .models import Producto


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "datos", "marca", "datos_precio", "coloreado")
    # ordering = ("id", "nombre")
    search_fields = ("datos", "marca", "categoria")
    # list_editable = ("stock",)
    list_display_links = ("datos",)
    list_filter = ("categoria",)
    list_per_page = 10
    # Opciones avanzadas
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "datos",
                    "imagen",
                    "marca",
                    "categoria",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse", "wide", "extrapretty"),
                "fields": (
                    "datos_precio",
                    "coloreado",
                ),
            },
        ),
    )

    def datos(self, obj):
        return obj.nombre.upper()

    def datos_precio(self, obj):
        return obj.precio

    datos.short_description = "PRODUCTOS"
    datos.empty_value_display = "???"
    datos.admin_order_field = "nombre"
    datos_precio.short_description = "PRECIO (S/.)"
    Producto.coloreado.short_description = "STOCK"
