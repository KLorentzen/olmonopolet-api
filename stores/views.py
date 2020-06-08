from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store
from rest_framework import generics

# Create your views here.
class StoreList(generics.ListAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer