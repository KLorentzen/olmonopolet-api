from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from olmonopolet.untappd_scraper import rating
from untappd.models import Rating, UntappdMapping

class Command(BaseCommand):
    help = 'Update Untappd Beer Rating'

    def handle(self, *args, **options):
        # Get verified Beer Mappings
        mappings = UntappdMapping.objects.filter(verified=True)
        
        for mapping in mappings:
            
            untappd = rating.get_rating(mapping.url)

            obj = Rating.objects.update_or_create(
                beer_id = mapping.beer_id,
                defaults={
                    'rating': untappd["rating"],
                    'num_ratings': untappd["num_regs"],
                    'check_in_total': untappd["check_in_total"],
                    'check_in_unique': untappd["check_in_unique"]
                }
            )
            self.stdout.write(f"Finner rating for {mapping.beer_id.name}")

        return