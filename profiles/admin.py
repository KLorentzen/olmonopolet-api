from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'premium', 'untappd_username', 'untappd_sync_date')
    search_fields = ('user',)

# Register your models here.
admin.site.register(Profile,ProfileAdmin)
