from .views import QuoteToPDFView, QuoteView
from django.urls import path, include  # add this

urlpatterns = [
    path("prospetto-quote", QuoteView.as_view(), name='generate-quote'),
    path("Quote_PDF", QuoteToPDFView.as_view(), name='Quote_PDF'),
]