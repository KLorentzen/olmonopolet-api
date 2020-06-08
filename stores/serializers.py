from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('store_id','name','category','city','street_address', 'postalcode')
        model = Store