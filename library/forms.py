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
    metodo_pago = forms.ChoiceField(
        choices=[("tarjeta", "Tarjeta de crédito"), ("efectivo", "Efectivo")]
    )
