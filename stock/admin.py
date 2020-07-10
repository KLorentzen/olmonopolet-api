from django.contrib import admin
from.models import BeerStock


class BeerStockAdmin(admin.ModelAdmin):
    list_display = ('beer_id','store_id', 'product_stock', 'restock_qty', 'restock_date', 'out_of_stock_date', 'last_updated')
    

# Register your models here.
admin.site.register(BeerStock,BeerStockAdmin)