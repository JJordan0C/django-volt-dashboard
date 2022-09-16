# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from .views import del_user, user_list, register_user

urlpatterns = [
    path('user-list', user_list, name="user-list"),
    path('create-user', register_user, name="create-user"),
    path('delete-user', del_user, name="delete-user"),
]