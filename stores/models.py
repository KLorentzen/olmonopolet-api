from django.db import models

# Create your models here.
class Store(models.Model):
    '''Vinmonopolet stores'''
    store_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    category = models.IntegerField(help_text='Store category, higher number is better quality',blank=True)
    city = models.CharField( max_length=250)
    street_address = models.CharField( max_length=250)
    postalcode = models.IntegerField()
    latitude = models.FloatField(help_text='GPS latitude', default=0.0)
    longitude = models.FloatField(help_text='GPS longitude', default=0.0)
    active = models.BooleanField(help_text='Is this store active on Ølmonopolet?', default=False)

    def __str__(self):
        return self.name
    