from django.urls import path, include
from .views import BeerStockListAPIView

urlpatterns = [
    path('',BeerStockListAPIView.as_view()),
]
