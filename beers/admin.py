from django.contrib import admin
from .models import Beer,Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','main_category','added_date')
    search_fields = ('product_id',)



class BeerAdmin(admin.ModelAdmin):
    list_display = ('name','brewery','style','alc_volume','selection','status','buyable','launch_date','added_date', 'last_updated')
    search_fields = ('name',)
    


# Register your models here.
admin.site.register(Beer,BeerAdmin)
admin.site.register(Product,ProductAdmin)

