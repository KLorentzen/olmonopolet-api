from django.shortcuts import render
from .models import Beer
from .serializers import BeerSerializer
from rest_framework import generics
# Create your views here.

class BeerList(generics.ListAPIView):
    queryset=Beer.objects.all()
    serializer_class=BeerSerializer