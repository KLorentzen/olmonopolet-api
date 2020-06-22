from django.db import models

# Create your models here.
class Product(models.Model):
    '''
    Utility model holding all product id's fetched from Vinmonopolet.
    Products include categories other than "øl".
    '''
    product_id = models.IntegerField(primary_key=True)
    main_category = models.CharField(max_length=250)

    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return str(self.product_id)


class Beer(models.Model):
    beer_id = models.OneToOneField(Product, to_field='product_id', on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=250)
    brewery = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    style = models.CharField(help_text="Beer style listed at Vinmonopolet",max_length=250, blank=True)
    alc_volume = models.FloatField(help_text="Alcohol volume in %", null=True,blank=True)
    price = models.FloatField(help_text="Product prize in NOK", default= 0.00,  blank=True)
    volume = models.FloatField(help_text="Volume in liters",null=True ,blank=True)
    selection = models.CharField(help_text='Product selection and ordering range',max_length=250, blank=True)
    url = models.URLField(help_text='URL extension to https://vinmonopolet.no',max_length=250, blank=True)

    
    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

    