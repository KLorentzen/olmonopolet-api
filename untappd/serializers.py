from rest_framework import serializers
from .models import Untappd, UntappdMapping

class UntappdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('beer_id',
                'url',
                'brewery',
                'brewery_url',
                'style',
                'description',
                'img_url',
                'rating', 
                'img_url',
                'num_ratings',
                'check_in_total',
                'check_in_unique',
                'last_updated')
        model = Untappd

class UntappdMappingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('beer_id',
                'untappd_id',
                'name',
                'url')
        model = UntappdMapping