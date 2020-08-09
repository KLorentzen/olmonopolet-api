# Denne management cmd skal benyttes til å mappe VMÅ->Untappd
from django.core.management.base import BaseCommand
from beers.models import Beer
from untappd.models import UntappdMapping
from olmonopolet.untappd_scraper import mapping 
from datetime import datetime

class Command(BaseCommand):
    help = '''
    Find mapping between Beers at Vinmonopolet and Untappd.  
    Beers will be automatically matched if a single search result is found on Untappd.  
    A maximum of 100 searches per hour is used to avoid blocking as this equals the rate limiting employed by the Untappd API.  
    Hence, this management command can only be executed once per hour.
    '''

    def handle(self, *args, **options):
        # Log when the job is executed
        self.stdout.write(f"Updating Beer mappings @ {datetime.now()}")

        SEARCH_COUNT = 0
        SEARCH_LIMIT = 200
        # Retrieve all Beers in DB that does not have an UntappdMapping, using related_name
        unmapped_beers = Beer.objects.filter(mappings = None)

        self.stdout.write(f"Number of unmapped beers: {unmapped_beers.count()}")

        for beer in unmapped_beers:
            untappd_mapping = mapping.find_untappd_mapping(beer.name, SEARCH_COUNT, SEARCH_LIMIT)
            SEARCH_COUNT = untappd_mapping['searches']
            
            # Log mapping process and monitor that number of searches does not exceed limit
            self.stdout.write(f"Mapping '{beer.name}' with matching status: {untappd_mapping['match']}. Number of searches performed: {untappd_mapping['searches']}")
            
            mapping_obj = UntappdMapping.objects.create(
                beer_id = beer,
                untappd_id = untappd_mapping['id'],
                name = untappd_mapping['name'],
                url = untappd_mapping['url'],
                auto_match = untappd_mapping['match']
                )

            if SEARCH_COUNT > SEARCH_LIMIT:
                break

        return