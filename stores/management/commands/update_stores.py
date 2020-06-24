from django.core.management.base import BaseCommand
from stores.models import Store
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import stores as vmp_api_stores 

class Command(BaseCommand):
    help = 'Update Vinmonopolet stores'

    def handle(self, *args, **options):
        # Used for logging
        new_stores = 0
        
        # Get list of all stores in database
        db_stores = list(Store.objects.values_list('store_id', flat=True))

        # Retrieve all Vinmonopolet stores
        all_stores = vmp_api_stores.get_all_stores()

        for store in all_stores:
            
            # Only add the store if it does not exist in the database
            if int(store["storeId"]) in db_stores:
                pass
            else:
                
                try:
                    # TODO: Add all stores when testing is completed
                    # Only use Molde (storeId=244) for testing
                    if int(store["storeId"]) in (244,245):
                        new_obj = Store.objects.create(
                            store_id = store["storeId"],
                            name = store["storeName"],
                            category = store["category"],
                            city = store["address"]["city"],
                            street_address = store["address"]["street"],
                            postalcode = store["address"]["postalCode"]
                        )

                        new_stores += 1
                except ValueError as err:
                    self.stdout.write(f"Could not insert store: {store['storeId']}")


        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_stores} new stores.")

        return