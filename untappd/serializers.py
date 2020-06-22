from rest_framework import serializers
from .models import Rating, UntappdMapping

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('beer_id', 'rating', 'num_ratings', 'check_in_total', 'check_in_unique', 'last_updated')
        model = Rating

class UntappdMappingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('beer_id', 'untappd_id', 'name', 'url')
        model = UntappdMapping