from django.contrib import admin
from .models import DetallePedido, PaymentInfo, Pedido, Producto, Categoria
from django.utils.html import format_html

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # readonly_fields = ("estado_stock",)
    list_display = ("id", "nombre", "marca", "precio", "estado_stock")
    # ordering = ("id", "nombre")
    search_fields = ("nombre", "marca", "categoria")
    # list_editable = ("stock",)
    list_display_links = ("nombre",)
    list_filter = ("categoria",)
    list_per_page = 10
    # Opciones avanzadas
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nombre",
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
                    "precio",
                    "stock",
                ),
            },
        ),
    )

    def nombre(self, obj):
        return obj.nombre.upper()

    def precio(self, obj):
        return obj.precio

    nombre.short_description = "PRODUCTOS"
    nombre.empty_value_display = "???"
    nombre.admin_order_field = "nombre"
    precio.short_description = "PRECIO (S/.)"
    # Producto.stock.short_description = "STOCK"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "descripcion",
    )  # Personaliza los campos que se muestran en la lista
    search_fields = ("nombre", "descripcion")  # Agrega campos de búsqueda si lo deseas
    list_filter = ("nombre",)  # Agrega filtros si es necesario


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "age", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


UserAdmin.list_display += ("age", "phone_number")
# Registra el modelo User con la clase de administración personalizada
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "total",
        "estado",
    )
    readonly_fields = (
        "id",
        "usuario",
        "total",
        "estado",
    )
    list_filter = ("estado",)
    search_fields = ("id", "usuario__username")


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "producto", "cantidad", "subtotal")
    readonly_fields = (
        "pedido",
        "producto",
        "cantidad",
        "subtotal",
    )
    list_filter = ("pedido__estado", "producto__categoria")
    search_fields = ("pedido__id", "producto__nombre")


admin.site.register(PaymentInfo)
