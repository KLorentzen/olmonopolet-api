from django.shortcuts import render
from rest_framework import generics
from .serializers import RatingSerializer, UntappdMappingSerializer
from .models import Rating, UntappdMapping

# Create your views here.

class RatingList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filterset_fields = ['beer_id']

class RatingDetail(generics.RetrieveAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = 'beer_id'

class MappingList(generics.ListAPIView):
    queryset = UntappdMapping.objects.filter(verified=True)
    serializer_class = UntappdMappingSerializer
    filterset_fields = ['beer_id']