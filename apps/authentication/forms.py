# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from apps.authentication.models import User, Shop


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
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


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cognome",
                "class": "form-control"
            }
        ))
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
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id": "passwUser",
                "readonly": "readonly"
            }
        ))
    
    DEALER_CHOICES =(
    (9, "Goldbet"),
    (11, "Snai"),
    (13, "Eurobet"),
    (14, "Planetwin"),
    (15, "Stanleybet"),
    )
    
    dealer_id = forms.ChoiceField(
        choices = DEALER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password', 'dealer_id')

class CreateShopForm(forms.ModelForm):
    s_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome Negozio",
                "class": "form-control"
            }
        ))
    
    s_tel = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Telefono Negozio",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Shop
        fields = ('s_name', 's_tel')


class EditShopForm(forms.ModelForm):
    s_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome Negozio",
                "class": "form-control"
            }
        ))
    
    s_tel = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Telefono Negozio",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Shop
        fields = ('s_name', 's_tel')
        
        
class EditUserForm(forms.ModelForm):
    user_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cognome",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id": "passwUser",
                "readonly": "readonly"
            }
        ))
    
    DEALER_CHOICES =(
    (9, "Goldbet"),
    (11, "Snai"),
    (13, "Eurobet"),
    (14, "Planetwin"),
    (15, "Stanleybet"),
    )
    
    dealer_id = forms.ChoiceField(
        choices = DEALER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password', 'dealer_id')