from django.core.management.base import BaseCommand
from stores.models import Store
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import stores as vmp_api_stores 
import httpx

class Command(BaseCommand):
    help = 'Update Vinmonopolet stores'

    def handle(self, *args, **options):
        # Used for logging
        new_stores = 0
        
        # Get list of all stores in database
        db_stores = list(Store.objects.values_list('store_id', flat=True))

        # Instantiate httpx Client
        with httpx.Client() as client:
            # Retrieve all Vinmonopolet stores
            all_stores = vmp_api_stores.get_all_stores(client)

        for store in all_stores:
            
            # Only add the store if it does not exist in the database
            if int(store["storeId"]) in db_stores:
                pass
            else:
                
                try:
                    new_obj = Store.objects.create(
                        store_id = store["storeId"],
                        name = store["storeName"],
                        category = store["category"],
                        city = store["address"]["city"],
                        street_address = store["address"]["street"],
                        postalcode = store["address"]["postalCode"],
                        latitude = store["address"]["gpsCoord"].split(';')[0],
                        longitude = store["address"]["gpsCoord"].split(';')[1],
                    )

                    new_stores += 1
                except Exception as err:
                    self.stdout.write(f"Could not insert store: {store['storeId']}")

        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_stores} new stores.")

        return