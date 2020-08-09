from django.contrib import admin
from .models import Untappd, UntappdMapping

# Register your models here.

class UntappdAdmin(admin.ModelAdmin):
    list_display = ('beer_id',
                    'brewery',
                    'style',
                    'rating',
                    'check_in_unique',
                    'last_updated')   

class UntappdMappingAdmin(admin.ModelAdmin):
    list_display = ('beer_id',
                    'untappd_id',
                    'auto_match',
                    'verified',
                    'last_updated')    


admin.site.register(Untappd, UntappdAdmin)
admin.site.register(UntappdMapping, UntappdMappingAdmin)