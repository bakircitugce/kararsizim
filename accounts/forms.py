import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="E-posta")
    username = forms.CharField(label="Kullanıcı adı", max_length=20)
    password1 = forms.CharField(label="Parola", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Parola (tekrar)", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Bu e-posta zaten kayıtlı.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
            raise ValidationError(
                "Kullanıcı adı 3-20 karakter olmalı; sadece harf, rakam ve alt çizgi içerebilir."
            )
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Bu kullanıcı adı alınmış.")
        return username


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-posta")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)

    error_messages = {"invalid_login": "E-posta veya parola hatalı."}

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        self.user_cache = authenticate(
            self.request,
            username=cleaned_data.get("email", "").strip().lower(),
            password=cleaned_data.get("password"),
        )
        if self.user_cache is None:
            raise ValidationError(self.error_messages["invalid_login"])
        return cleaned_data

    def get_user(self):
        return self.user_cache
