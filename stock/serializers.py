from rest_framework import serializers
from .models import BeerStock

class BeerStockSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('beer_id','store_id','product_stock','last_updated','created')
        model = BeerStock