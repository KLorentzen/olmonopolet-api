from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','untappd_username','premium')
    search_fields = ('user',)

# Register your models here.
admin.site.register(Profile,ProfileAdmin)
