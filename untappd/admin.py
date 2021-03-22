from django.contrib import admin
from .models import Untappd, UntappdMapping

# Register your models here.

class UntappdAdmin(admin.ModelAdmin):
    list_display = ('beer_id',
                    'brewery',
                    'style',
                    'rating',
                    'num_ratings',
                    'last_updated')   
    search_fields = ('beer_id__name', )

class UntappdMappingAdmin(admin.ModelAdmin):
    list_display = ('beer_id',
                    'untappd_id',
                    'auto_match',
                    'verified',
                    'last_updated')   
    search_fields = ('beer_id__name', )

admin.site.register(Untappd, UntappdAdmin)
admin.site.register(UntappdMapping, UntappdMappingAdmin)