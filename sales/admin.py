from django.contrib import admin
from .models import DailySale
# Register your models here.

class DailySaleAdmin(admin.ModelAdmin):
    list_display = ('beer_id', 'store_id','sales_day','beers_sold','last_updated')
    list_filter = ("sales_day",)
    search_fields = ('beer_id__name', )

admin.site.register(DailySale, DailySaleAdmin)
