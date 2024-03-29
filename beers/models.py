from django.db import models
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Product(models.Model):
    '''
    Utility model holding all product id's fetched from Vinmonopolet.
    Products include categories other than "øl".
    '''
    product_id = models.BigIntegerField(primary_key=True)
    main_category = models.CharField(max_length=250)

    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ["-added_date"]
        
    def __str__(self):
        return str(self.product_id)


class Beer(models.Model):
    beer_id = models.OneToOneField(Product, to_field='product_id', on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=250)
    brewery = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    style = models.CharField(help_text="Beer style listed at Vinmonopolet",max_length=250,null=True, blank=True)
    alc_volume = models.FloatField(help_text="Alcohol volume in %", null=True,blank=True)
    price = models.FloatField(help_text="Product prize in NOK", default= 0.00,  blank=True)
    volume = models.FloatField(help_text="Volume in liters",null=True ,blank=True)
    selection = models.CharField(help_text='Product selection and ordering range',max_length=250, null=True, blank=True)
    url = models.URLField(help_text='Full URL to beer at Vinmonopolet',max_length=250, blank=True)

    status = models.CharField(max_length=250, blank=True)
    buyable = models.BooleanField(help_text='Is beer available for purchase?', default=False)
    launch_date = models.DateField(help_text='Date when beer was launched', null=True, blank=True)
    
    added_date = models.DateField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-launch_date', "-added_date"]
    
    def __str__(self):
        return self.name

    def get_image_url(self):
        '''
        Choose the correct image url for a Beer 
          1. Return Untappd image URL
          2. Return default image URL (static file)
        '''

        try:
            if self.untappd.img_url != 'https://untappd.akamaized.net/site/assets/images/temp/badge-beer-default.png':
                # Use Untappd image URL in cases it is not the 'default' Untappd Beer Image
                return self.untappd.img_url
            else:
                return static('images/MissingBeerImage.png')
        except ObjectDoesNotExist:
            return static('images/MissingBeerImage.png')

    