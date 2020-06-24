from django.shortcuts import render
from rest_framework import generics
from .models import DailySale
from .serializers import DailySaleSerializer

# Create your views here.
class DailySaleList(generics.ListAPIView):
    queryset = DailySale.objects.all()
    serializer_class = DailySaleSerializer
    filterset_fields = ['store_id', 'beer_id', 'sales_day']