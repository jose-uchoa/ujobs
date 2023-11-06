from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    register_choices = (
        ("default", "Selecione uma opção"),
        ("candidate", "Candidato"),
        ("company", "Recrutador"),
    )
    register_as = forms.ChoiceField(
        label="Cadastrar como",
        choices=register_choices,
        widget=forms.Select(
            attrs={"id": "select-style", "autofocus": "autofocus"},
        ),
    )

    full_name = forms.CharField(
        label="Nome completo",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ex. José Uchôa",
            }
        ),
    )

    email = forms.EmailField(
        label="Informe seu e-mail",
        widget=forms.EmailInput(
            attrs={"placeholder": "Digite seu e-mail"},
        ),
    )

    password1 = forms.CharField(
        label="Definir senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
    )

    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Repita sua senha"}),
    )

    error_messages = {
        "password_mismatch": "As senhas não correspondem, tente novamente",
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está sendo usado")
        return email

    class Meta:
        model = User
        fields = [
            "register_as",
            "full_name",
            "email",
            "password1",
            "password2",
        ]


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Informe seu e-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Digite seu e-mail",
                "autofocus": "autofocus",
            },
        ),
    )
    password = forms.CharField(
        label="Agora, informe sua senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
    )
