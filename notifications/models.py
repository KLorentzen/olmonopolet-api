from django.db import models
from django.contrib.auth.models import User
from stores.models import Store

# Create your models here.
class EmailNotification(models.Model):
    '''
    Model containing user preferences with regards to how they receive email notifications.
    '''
    
    username = models.ForeignKey(User, to_field='username', verbose_name='Users', related_name='notification', on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, verbose_name='Stores', to_field='store_id',related_name='notification', on_delete=models.CASCADE, help_text='Store which the user want to receive notifications for')

    store_updates = models.BooleanField(help_text='Should the user receive email notification when product stock is updated for chosen store?', default=False)

    class Meta:
        verbose_name_plural = 'Email Notifications'
        ordering = ['-username']
    def __str__(self):
        return self.username.username
    