from django.contrib import admin
from .models import Producto


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "marca", "precio", "stock")
    # ordering = ("id", "nombre")
    search_fields = ("nombre", "marca", "categoria")
    # list_editable = ("stock",)
    list_display_links = ("nombre",)
    list_filter = ("categoria",)
    list_per_page = 10
