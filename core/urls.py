# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from django.contrib import admin
from django.urls import path, include  # add this
from apps.quote.views import DashboardView

urlpatterns = [
    # path('admin/', admin.site.urls),          # Django admin route
    path("auth/", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    # path("", include("apps.home.urls")),
    path("dashboard", DashboardView.as_view(), name='dashboard'),
    path("quote/", include("apps.quote.urls")),
]
