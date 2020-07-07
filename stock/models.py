from django.db import models
from beers.models import Beer
from stores.models import Store

# Create your models here.
class BeerStock(models.Model):
    '''
    Beer stock available at Vinmonopolet stores.
    '''
    beer_id = models.ForeignKey(Beer, verbose_name="Beers", on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, verbose_name="Stores",on_delete=models.CASCADE)
    product_stock = models.IntegerField()
    
    restock_date = models.DateField(help_text='Date when product was last re-stocked',auto_now=False, auto_now_add=False)
    out_of_stock_date = models.DateField(help_text='Date when product was sold out (null if in stock)', auto_now=False, auto_now_add=False, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField( auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Beer Stock'

    def __str__(self):
        # Return the name of the beer_id based on relationship
        return self.beer_id.name
    