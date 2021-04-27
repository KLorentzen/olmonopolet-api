from django.core.management.base import BaseCommand
from django.db.models import F, Q
from profiles.models import Profile
from olmonopolet.untappd_api import user as untappd_user
from datetime import datetime

class Command(BaseCommand):
    help = '''
    Update Untappd beer check-ins for all Olmonopolet users which have an Untappd username defined in their Profile.  
    Users are updated in order where last synced user is synced first.  
    '''


    def handle(self, *args, **options):

        # Get all Profiles who have set their Untappd Username(UT Username='' as default) ordered by last Untappd synced profile
        user_profiles = Profile.objects.exclude(Q(untappd_username='')).order_by(F('untappd_sync_date').asc(nulls_first=True))
        
        self.stdout.write(f"Updating Untappd User Check-Ins @ {datetime.now()}")

        for profile in user_profiles:
            beers_syncronized, sync_status, remaining_requests = untappd_user.sync_untappd(profile.user)

            if sync_status:
                self.stdout.write(f"Syncronized Untappd for {profile.user}, {len(beers_syncronized)} check-ins to Untappd were added.")
                self.stdout.write(f"Remaining requests: {remaining_requests}.")
            else:
                self.stdout.write(f"Maximum number of requests towards Untappd performed.")
                break

        return