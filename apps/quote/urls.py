from .views import QuoteView, TestView

from django.urls import path, include  # add this

urlpatterns = [
    path("test", TestView.as_view(), name='test'),
    path("generate-quote", QuoteView.as_view(), name='generate-quote'),
]