from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store
from rest_framework import generics
from django.views.generic import ListView


# Regular Views
class StoreListView(ListView):
    model=Store
    template_name='home.html'
    context_object_name='stores'
    ordering=['-category', 'name']

# API Views
class StoreListAPIView(generics.ListAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer