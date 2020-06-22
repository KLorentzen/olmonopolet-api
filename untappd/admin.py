from django.contrib import admin
from .models import Rating, UntappdMapping

# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    list_display = ('beer_id','rating','num_ratings','check_in_unique', 'check_in_total', 'last_updated')   

class UntappdMappingAdmin(admin.ModelAdmin):
    list_display = ('beer_id', 'untappd_id', 'verified', 'last_updated')    


admin.site.register(Rating, RatingAdmin)
admin.site.register(UntappdMapping, UntappdMappingAdmin)