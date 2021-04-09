from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''
    Profile associated with User model.  
    Automatically added from signal when User is created.
    '''
    user = models.OneToOneField(User, verbose_name='User',related_name='profiles',on_delete=models.CASCADE)
    premium = models.BooleanField(help_text='Is user premium?', default=False)

    # Untappd Fields
    untappd_username = models.CharField(help_text='Untappd username', max_length=250, blank=True)
    untappd_avatar_url = models.URLField(help_text='URL to Avatar used on Untappd', max_length=256, blank=True, default='')
    untappd_sync_date = models.DateTimeField(help_text='Time when Profile was last synced with Untappd',blank=True, null=True)

    def __str__(self):
        return self.user.username
    