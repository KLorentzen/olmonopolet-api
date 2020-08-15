from django.contrib import admin
from .models import EmailNotification

# Register your models here.
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'store_id',
                    'store_updates')    


admin.site.register(EmailNotification, EmailNotificationAdmin)