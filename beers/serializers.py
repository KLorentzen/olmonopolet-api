from rest_framework import serializers
from .models import Beer

class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('name','brewery','style','alc_volume','volume','url','added_date')
        model = Beer