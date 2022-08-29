from .views import TestView

from django.urls import path, include  # add this

urlpatterns = [
    path("test", TestView.as_view(), 'test')
]