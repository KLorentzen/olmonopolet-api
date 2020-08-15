from django.contrib import admin
from .models import Beer,Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','main_category','added_date')


class BeerAdmin(admin.ModelAdmin):
    list_display = ('name','brewery','style','alc_volume','selection','added_date')
    search_fields = ('name',)
    


# Register your models here.
admin.site.register(Beer,BeerAdmin)
admin.site.register(Product,ProductAdmin)

