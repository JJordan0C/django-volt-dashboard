# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from apps.authentication.models import Shop, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CreateShopForm, LoginForm, CreateUserForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard") if user.is_superuser else redirect("/quote/prospetto-quote")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    dealer = request.user.get_dealer()
    msg = None
    success = False
    
    if request.method == "POST":
        shopForm = CreateShopForm(request.POST)
        userForm = CreateUserForm(request.POST)
        if shopForm.is_valid() and userForm.is_valid():
            shop = shopForm.save()
            user = userForm.save()
            user.shop = shop
            userForm.save()
            # username = form.cleaned_data.get("username")
            # first_name = form.cleaned_data.get("first_name")
            # last_name = form.cleaned_data.get("last_name")
            # raw_password = form.cleaned_data.get("password1")
            # dealer = form.cleaned_data.get("dealer")
            # shop_name = form.cleaned_data.get("shop_name")
            # shop_number = form.cleaned_data.get("shop_number")
            #user = authenticate(username=username, first_name=first_name, last_name=last_name, password=raw_password, dealer=dealer, shop_name=shop_name, shop_number=shop_number)

            msg = 'User created'
            success = True
            return redirect("user-list")
            
        else:
            msg = 'Form is not valid'
    else:
        shopForm = CreateShopForm()
        userForm = CreateUserForm()
        
    context = {
        'userForm': userForm,
        'shopForm': shopForm,
        'msg': msg,
        'success': success,
        'dealer':dealer
        }

    return render(request, "user/create_user.html", context=context)

def del_user(request):
    user_id = request.POST.get('user_id')
    print(request.POST.get('user_id'))
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("user-list")

def user_list(request):
    dealer = request.user.get_dealer()
    users = User.objects.all()
    shops = Shop.objects.all()
    
    context = {
        'users': users,
        'shops' : shops,
        'dealer': dealer
        }
    return render(request, "user/user_list.html", context=context)

def edit_user(request):
    dealer = request.user.get_dealer()
    msg = None
    success = False
    
    if request.method == "POST":
        shopForm = CreateShopForm(request.POST)
        userForm = CreateUserForm(request.POST)
        if shopForm.is_valid() and userForm.is_valid():
            shop = shopForm.save()
            user = userForm.save()
            user.shop = shop
            userForm.save()
            msg = 'User modified'
            success = True
            return redirect("user-list")
            
        else:
            msg = 'Form is not valid'
    else:
        shopForm = CreateShopForm()
        userForm = CreateUserForm()
        
    context = {
        'userForm': userForm,
        'shopForm': shopForm,
        'msg': msg,
        'success': success,
        'dealer':dealer
        }

    return render(request, "user/create_user.html", context=context)