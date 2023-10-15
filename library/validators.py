from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# Validaciones
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
