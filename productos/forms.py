from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido, DatosCliente

class DatosClienteForm(forms.ModelForm):
    class Meta:
        model = DatosCliente
        fields = [
            'nombre', 'nit', 'direccion', 'telefono',
            'tipo_pago',
            'tarjeta_numero', 'tarjeta_codigo', 'tarjeta_expira',
            'transferencia_autorizacion', 'transferencia_cuenta',
        ]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'cantidad', 'tipo_pago']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False, label="Nombre")
    last_name = forms.CharField(required=False, label="Apellido")
    email = forms.EmailField(required=True, label="Email")
    avatar = forms.ImageField(required=False, label="Foto de perfil")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "avatar")