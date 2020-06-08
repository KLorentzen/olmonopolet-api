from django.db import models

# Create your models here.
class Store(models.Model):
    '''Vinmonopolet stores'''
    store_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    category = models.IntegerField(help_text='Store category, higher number is better quality')
    city = models.CharField( max_length=250)
    address = models.CharField( max_length=250)

    def __str__(self):
        return self.name
    