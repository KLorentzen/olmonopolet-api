from django.db import models
from beers.models import Beer

# Create your models here.

class Rating(models.Model):
    '''
    Ratings from Untappd
    '''
    # TODO: change to one-to-one field?
    beer_id = models.ForeignKey(Beer, verbose_name='Beers',related_name='ratings',on_delete=models.CASCADE)
    rating = models.FloatField(help_text="Beer rating on Untappd", default=0)
    num_ratings = models.IntegerField(help_text="Number of ratings registered", default=0)
    check_in_total = models.IntegerField(default=0)
    check_in_unique = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField( auto_now_add=True)

    def __str__(self):
        # Return the name of the beer_id based on relationship
        return self.beer_id.name

class UntappdMapping(models.Model):
    '''
    Mapping between beers from Vinmonopolet and Untappd
    '''
    # TODO: change to one-to-one field?
    beer_id = models.ForeignKey(Beer, verbose_name='Beers',related_name='mappings',on_delete=models.CASCADE)
    untappd_id = models.IntegerField(help_text='Beer ID on Untappd')
    name = models.CharField(help_text='Name on Untappd.com', max_length=250)
    url = models.URLField(help_text='Full URL to beer on Untappd.com',max_length=250, blank=True)

    verified = models.BooleanField(help_text='Is mapping between Vinmonopolet and Untappd verified by admin?',default=False)

    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Untappd Mapping'
        verbose_name_plural = 'Untappd Mappings'

    def __str__(self):
        # Return the name of the beer_id based on relationship
        return self.beer_id.name