from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import *


class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(
        required=True,
        label="Edad",
        min_value=0,
        max_value=120,
        validators=[validate_age],
    )
    phone_number = forms.CharField(
        max_length=9,
        required=True,
        label="Numero telefonico",
        validators=[
            MinLengthValidator(9),
            validate_numeric_phone,
            validate_phone_starts_with_9,
        ],
    )
    first_name = forms.CharField(
        max_length=51,
        required=True,
        label="Nombres",
        validators=[validate_firstname_length, validate_firstname_letters_only],
    )
    last_name = forms.CharField(
        max_length=51,
        required=True,
        label="Apellidos",
        validators=[validate_lastname_length, validate_lastname_letters_only],
    )
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
        validators=[
            validate_allowed_domain,
            validate_unique_email,
            validate_max_username_email_length,
        ],
    )
    dni = forms.CharField(
        required=True,
        max_length=8,
        label="DNI",
        validators=[
            MinLengthValidator(8),
            validate_numeric_dni,
        ],
    )
    username = forms.CharField(
        max_length=31,
        required=True,
        label="Usuario",
        validators=[validate_username_length],
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            "age",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "dni",
            "username",
        )


class PedidoForm(forms.Form):
    metodo_pago = forms.ChoiceField(choices=[("tarjeta", "Tarjeta de crédito")])


class SimulatedPaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Número de tarjeta",
        max_length=16,
        validators=[MinLengthValidator(16), validate_numeric_tarjeta],
    )
    expiration_date = forms.CharField(
        label="Fecha de vencimiento (MM/YY)",
        max_length=5,
        help_text="Ejemplo: 12/25",
        validators=[validate_expiration_date],
    )
    security_code = forms.CharField(
        label="Código de seguridad (CVV)",
        max_length=3,
        validators=[MinLengthValidator(3), validate_numeric_cvv],
    )
    metodo_pago = forms.CharField(max_length=100)
