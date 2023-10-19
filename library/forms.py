from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True)
    phone_number = forms.CharField(max_length=9, required=True)
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required. 30 characters or fewer."
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text="Required. 30 characters or fewer"
    )
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            "age",
            "phone_number",
            "first_name",
            "last_name",
            "email",
        )


class PedidoForm(forms.Form):
    metodo_pago = forms.ChoiceField(choices=[("tarjeta", "Tarjeta de crédito")])


class SimulatedPaymentForm(forms.Form):
    card_number = forms.CharField(label="Número de tarjeta", max_length=20)
    expiration_date = forms.CharField(
        label="Fecha de vencimiento (MM/YY)", max_length=5, help_text="Ejemplo: 12/25"
    )
    security_code = forms.CharField(label="Código de seguridad (CVV)", max_length=4)
    metodo_pago = forms.CharField(max_length=100)
    num_doc = forms.IntegerField(max_value=99999999)
    # first_name = forms.CharField(
    #     max_length=30, help_text="Required. 30 characters or fewer."
    # )
    # last_name = forms.CharField(
    #     max_length=30, help_text="Required. 30 characters or fewer"
    # )

    # phone_number = forms.CharField(max_length=9)
