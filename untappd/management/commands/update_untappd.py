from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from olmonopolet.untappd_scraper import details
from untappd.models import Untappd, UntappdMapping

class Command(BaseCommand):
    help = 'Update Untappd Beer Details'

    def handle(self, *args, **options):
        # Get verified Beer Mappings
        mappings = UntappdMapping.objects.filter(verified=True)
        
        for mapping in mappings:
            
            untappd = details.get_beer_details(mapping.url)

            obj = Untappd.objects.update_or_create(
                beer_id = mapping.beer_id,
                url = mapping.url,
                defaults={
                    'brewery':untappd["brewery"],
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

        return