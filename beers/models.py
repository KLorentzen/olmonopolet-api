from django.db import models

# Create your models here.

class Beer(models.Model):
    # TODO: Add Product as foreign key?
    beer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    brewery = models.CharField(max_length=250, blank=True)
    style = models.CharField(help_text="Beer style",max_length=250, blank=True)
    alc_volume = models.FloatField(help_text="Alcohol volume in %", null=True,blank=True)
    volume = models.FloatField(help_text="Volume in liters",null=True ,blank=True)
    selection = models.CharField(max_length=250, blank=True)
    url = models.URLField(max_length=250, blank=True)

    
    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    '''
    Utility model holding all product id's fetched from Vinmonopolet.
    Products include categories other than "øl".
    '''
    product_id = models.IntegerField()
    main_category = models.CharField(max_length=250)

    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return str(self.product_id)
    