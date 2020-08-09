from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from olmonopolet.untappd_scraper import details
from untappd.models import Untappd, UntappdMapping
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Update Untappd Beer Details'

    def handle(self, *args, **options):
        # Get verified Beer Mappings
        mappings = UntappdMapping.objects.filter(auto_match=True) | UntappdMapping.objects.filter(verified=True)
        
        # Log when the job is executed
        start_time = datetime.now()
        self.stdout.write(f"Updating Untappd data @ {datetime.now()}")

        for mapping in mappings:
            
            untappd = details.get_beer_details(mapping.url)

            try:
                obj = Untappd.objects.update_or_create(
                    beer_id = mapping.beer_id,
                    url = mapping.url,
                    defaults={
                        'brewery': untappd["brewery"],
                        'brewery_url': 'https://www.untappd.com' + untappd["brewery_url"],
                        'style':untappd["style"],
                        'description': untappd["description"] if untappd["description"] else '',
                        'img_url':untappd["img_url"],
                        'rating': untappd["rating"],
                        'num_ratings': untappd["num_regs"],
                        'check_in_total': untappd["check_in_total"],
                        'check_in_unique': untappd["check_in_unique"]
                    }
                )
                self.stdout.write(f"Oppdaterer Untappd data for {mapping.beer_id.name}")
            except Exception as err:
                self.stdout.write(f"Could not create or update Untappd data for '{mapping.beer_id.name}'. Got the following exception: {err} ")
            
            # Reduce load on Untappd and DB
            time.sleep(0.5)
        
        end_time = datetime.now()
        self.stdout.write(f"Untappd update took {end_time - start_time} seconds")
        
        return