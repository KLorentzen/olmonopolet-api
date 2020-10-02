from django.contrib import admin
from.models import BeerStock, WatchList


class BeerStockAdmin(admin.ModelAdmin):
    list_display = ('beer_id','store_id', 'product_stock', 'restock_qty', 'restock_date', 'out_of_stock_date', 'last_updated')
    search_fields = ('beer_id__name', )

class WatchListAdmin(admin.ModelAdmin):
    list_display = ('beer_id','created') 
    search_fields = ('beer_id__name', )
    autocomplete_fields = ('beer_id', )

# Register your models here.
admin.site.register(BeerStock,BeerStockAdmin)
admin.site.register(WatchList,WatchListAdmin)