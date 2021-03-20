from django.db import models
from beers.models import Beer

# Create your models here.
class Untappd(models.Model):
    '''
    Details from Untappd
    '''
    beer_id = models.OneToOneField(Beer, verbose_name='Beers',related_name='untappd',on_delete=models.CASCADE)
    url = models.URLField(help_text='Full URL to beer on Untappd.com',max_length=250)
    brewery = models.CharField(max_length=250)
    brewery_url = models.URLField(help_text='Full URL to brewery on Untappd.com', max_length=250)
    style = models.CharField(help_text='Beer style listed on Untappd', max_length=250)
    description = models.TextField(blank=True)
    img_url = models.URLField(help_text='Thumbnail URL on Untappd.com', blank=True)
    rating = models.FloatField(help_text="Beer rating on Untappd", default=0)
    num_ratings = models.IntegerField(help_text="Number of ratings registered", default=0)
    check_in_total = models.IntegerField(default=0)
    check_in_unique = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Untappd'
        verbose_name_plural = 'Untappd'
        ordering = ['-rating']

    def __str__(self):
        # Return the name of the beer_id based on relationship
        return self.beer_id.name

class UntappdMapping(models.Model):
    '''
    Mapping between beers from Vinmonopolet and Untappd
    '''
    beer_id = models.OneToOneField(Beer, verbose_name='Beers',related_name='mappings',on_delete=models.CASCADE)
    untappd_id = models.IntegerField(help_text='Beer ID on Untappd')
    name = models.CharField(help_text='Name on Untappd.com', max_length=250)
    url = models.URLField(help_text='Full URL to beer on Untappd.com',max_length=250, blank=True)
    auto_match = models.BooleanField(help_text='Was mapping obtained automatically?', default=False)
    verified = models.BooleanField(help_text='Is mapping between Vinmonopolet and Untappd verified by admin?', default=False)

    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Untappd Mapping'
        verbose_name_plural = 'Untappd Mappings'

    def __str__(self):
        # Return the name of the beer_id based on relationship
        return self.beer_id.name