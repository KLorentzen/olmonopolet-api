from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store
from rest_framework import generics
from django.views.generic import TemplateView


# Regular Views
class StoreView(TemplateView):
    template_name='home.html'

# API Views
class StoreListAPIView(generics.ListAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer