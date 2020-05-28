from django.db import models

# Create your models here.

class Beer(models.Model):
    beer_ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    brewery = models.CharField(max_length=250)
    style = models.CharField(max_length=250)
    alc_volume = models.FloatField()
    volume = models.FloatField()
    url = models.URLField(max_length=250)
    
    added_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name