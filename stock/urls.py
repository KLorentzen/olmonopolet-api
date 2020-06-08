from django.urls import path, include
from .views import BeerStockList

urlpatterns = [
    path('',BeerStockList.as_view()),
]
