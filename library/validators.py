import re
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


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


def validate_descripcion_cate_length(value):
    if not 1 <= len(value) <= 100:
        raise ValidationError(
            _("La descripcion debe tener entre 1 y 100 caracteres."),
            code="invalid_descrip_cate_length",
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


# REGISTRO CLIENTE

# Validaciones first_name


def validate_firstname_length(value):
    if not 3 <= len(value) <= 50:
        raise ValidationError(
            _("El nombre debe tener entre 3 y 50 caracteres."),
            code="invalid_nombre_length",
        )


def validate_firstname_letters_only(value):
    # Verifica si el valor contiene solo letras y espacios (sin caracteres especiales ni números)
    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            _("El nombre no debe contener caracteres especiales ni números."),
            code="invalid_marca_letters_only",
        )


# Validaciones last_name


def validate_lastname_length(value):
    if not 2 <= len(value) <= 50:
        raise ValidationError(
            _("El apellido debe tener entre 2 y 50 caracteres."),
            code="invalid_nombre_length",
        )


def validate_lastname_letters_only(value):
    # Verifica si el valor contiene solo letras y espacios (sin caracteres especiales ni números)
    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            _("El apellido no debe contener caracteres especiales ni números."),
            code="invalid_marca_letters_only",
        )


# Validaciones username
def validate_username_length(value):
    if not 1 <= len(value) <= 30:
        raise ValidationError(
            _("El usuario debe ser maximo de 30 caracteres."),
            code="invalid_nombre_length",
        )


# Validaciones de email


def validate_allowed_domain(value):
    allowed_domains = ["gmail.com", "outlook.com", "hotmail.com"]
    domain = value.split("@")[1]
    if domain not in allowed_domains:
        raise ValidationError("El dominio de correo electrónico no está permitido.")


def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("Esta dirección de correo electrónico ya está en uso.")


def validate_max_username_email_length(value):
    # Divide el correo electrónico en dos partes: nombre de usuario y dominio
    username, domain = value.split("@")
    if len(username) > 30:
        raise ValidationError(
            "El nombre de usuario no puede tener más de 30 caracteres."
        )


# validaciones edad
def validate_age(value):
    if not isinstance(value, int):
        raise ValidationError("La edad debe ser un número entero.")
    if value < 16:
        raise ValidationError("La edad debe ser mayor o igual a 16.")


# validaciones phone_number


def validate_numeric_phone(value):
    if not re.match(r"^\d{9}$", value):
        raise ValidationError(
            "El número de teléfono solo debe contener exactamente 9 DIGITOS. "
        )


def validate_phone_starts_with_9(value):
    if not value.startswith("9"):
        raise ValidationError("El número de teléfono debe comenzar con el número 9.")


# validaciones DNI
def validate_numeric_dni(value):
    if not re.match(r"^\d{8}$", value):
        raise ValidationError("El DNI debe contener exactamente 8 dígitos numéricos.")


def validate_numeric_tarjeta(value):
    if not re.match(r"^\d{16}$", value):
        raise ValidationError(
            "El Numero de tarjeta debe contener exactamente 16 dígitos numéricos."
        )


def validate_expiration_date(value):
    if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", value):
        raise ValidationError("Formato de fecha de vencimiento no válido.")

    exp_month, exp_year = map(int, value.split("/"))
    current_year = datetime.now().year % 100

    if exp_year < current_year or (
        exp_year == current_year and exp_month < datetime.now().month
    ):
        raise ValidationError("La fecha de vencimiento ha expirado.")


def validate_numeric_cvv(value):
    if not re.match(r"^\d{3}$", value):
        raise ValidationError(
            "El Codigo de seguridad debe contener exactamente 3 dígitos numéricos."
        )
