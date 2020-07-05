from django.shortcuts import render
from rest_framework import generics
from .serializers import UntappdSerializer, UntappdMappingSerializer
from .models import Untappd, UntappdMapping

# Create your views here.

class UntappdList(generics.ListAPIView):
    queryset = Untappd.objects.all()
    serializer_class = UntappdSerializer

class UntappdDetail(generics.RetrieveAPIView):
    queryset = Untappd.objects.all()
    serializer_class = UntappdSerializer
    lookup_field = 'beer_id'

class MappingList(generics.ListAPIView):
    queryset = UntappdMapping.objects.filter(verified=True)
    serializer_class = UntappdMappingSerializer
    filterset_fields = ['beer_id']