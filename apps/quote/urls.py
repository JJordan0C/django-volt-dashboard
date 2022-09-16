from .views import QuoteToPDFView, QuoteView, TestView
from django.urls import path, include  # add this

urlpatterns = [
    path("test", TestView.as_view(), name='test'),
    path("prospetto-quote", QuoteView.as_view(), name='generate-quote'),
    path("generate-quote-pdf", QuoteToPDFView.as_view(), name='generate-quote-pdf'),
]