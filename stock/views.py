from django.shortcuts import render
from rest_framework import generics
from .models import BeerStock
from .serializers import BeerStockSerializer

# Create your views here.
class BeerStockList(generics.ListAPIView):
    queryset = BeerStock.objects.all()
    serializer_class = BeerStockSerializer