from django.db import models
from beers.models import Beer
from stores.models import Store

# Create your models here.
class DailySale(models.Model):
    beer_id = models.ForeignKey(Beer, verbose_name='Beers',related_name='daily_sales', on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, verbose_name='Stores',related_name='daily_sales', on_delete=models.CASCADE)
    sales_day = models.DateField(auto_now_add=True)
    beers_sold = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Daily Sales'

    def __str__(self):
        return self.beer_id.name
    
