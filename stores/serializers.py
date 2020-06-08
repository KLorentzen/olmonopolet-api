from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('store_id','name','category','city','address')
        model = Store