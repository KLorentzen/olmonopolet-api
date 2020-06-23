from rest_framework import serializers
from .models import DailySale

class DailySaleSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('beer_id','store_id','sales_day','beers_sold','last_updated')
        model = DailySale