# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.authentication.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Conferma Password",
                "class": "form-control"
            }
        ))
    
    DEALER_CHOICES =(
    (0, "Goldbet"),
    (1, "Snai"),
    (2, "Eurobet"),
    (3, "Planetwin"),
    (4, "Stanleybet"),
    )
    
    dealer = forms.ChoiceField(
        choices = DEALER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )
    
    shop_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome Negozio",
                "class": "form-control"
            }
        ))
    
    shop_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Telefono Negozio",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'dealer', 'shop_name', 'shop_number')
