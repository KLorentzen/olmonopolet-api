from rest_framework import serializers
from .models import Beer

class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('beer_id','name','brewery','style','alc_volume','volume','selection','url','added_date')
        model = Beer