from django.core.management.base import BaseCommand
from beers.models import Product, Beer
from olmonopolet.vmp_api import products as vmp_api_products 
from datetime import datetime
from olmonopolet.vmp_api import beer_stock  


class Command(BaseCommand):
    help = '''
    Update Beer details from Vinmonopolet
    
    '''

    def handle(self, *args, **options):
        # Log when the job is executed
        self.stdout.write(f"Updating Beer details @ {datetime.now()}")
        start_time = datetime.now()
        
        # Verify that VMP is online before using the VMP api
        if not beer_stock.isVMPonline:
            self.stdout.write(f"Vinmonopolet is not available...")
            return

        beers = Beer.objects.all()

        for beer in beers:
            # Update Beer details from Vinmonopolet
            beer_details = vmp_api_products.get_product_details(beer.pk)
            
            # TODO: Add functionality to notify user if beer with stock becomes "buyable:True"

            try:
                updated_beer_obj, created = Beer.objects.update_or_create(
                    beer_id = beer,
                    defaults = {
                        'name' : beer_details["name"],
                        'alc_volume' : beer_details['alcohol']['value'],
                        'buyable' : beer_details["buyable"],
                        'status' : beer_details["status"],
                        'launch_date' : datetime.strptime(beer_details["expiredDate"],"%Y-%m-%d")
                    }
                )

                self.stdout.write(f"Updating beer details for: {updated_beer_obj.name}")

            except Exception as err:
                self.stdout.write(f"Could not update beer details for: {beer.name}")
                self.stdout.write(err)

            # Product stock is not to be updated if status is "Utgått" or "Utsolgt"
            # This is to reduce load on the system as these beers are not available for purchase
            # if updated_beer_obj.status not in ['utgatt', 'utsolgt']:


        self.stdout.write(f"Update of beer details took {datetime.now() - start_time} seconds")

        return