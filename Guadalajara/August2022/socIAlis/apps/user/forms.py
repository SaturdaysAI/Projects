from django import forms
from django.contrib.auth import authenticate
from datetime import date
from django.core.exceptions import ValidationError

from apps import user
from .models import User


my_default_errors = {
    'required': 'Este campo es requerido.',
    'invalid': 'Valor invalido.',
    'unique': 'Ya existe un usuario registrado con este correo.',
}


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Correo'
            }
        ),
        error_messages=my_default_errors 
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu nombre(s)'
            }
        ) 
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
