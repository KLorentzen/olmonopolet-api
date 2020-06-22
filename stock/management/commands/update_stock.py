from django.core.management.base import BaseCommand
from beers.models import Beer
from stock.models import BeerStock
from stores.models import Store
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import beer_stock  

class Command(BaseCommand):
    help = 'Update beer stock from Vinmonopolet'

    def handle(self, *args, **options):
        # Used for logging
        # new_products = 0
        
        # Retrieve all beers in database
        beers = Beer.objects.all()

        for beer in beers:

            # Get Stores which have had the beer in stock at some point
            old_stock = BeerStock.objects.filter(beer_id=beer).values_list("store_id",flat=True)
            
            # Get current stock from VMP
            stock_all_stores = beer_stock.get_stock_all_stores(beer.beer_id)
            
            # Store IDs of stores with stock > 0
            stores_with_stock = [int(i['name']) for i in stock_all_stores]

            # empty_stores = [beer for beer in current_stock if beer not in stores_with_stock]
            empty_stores = filter(lambda x: x not in stores_with_stock,old_stock)

            # TODO: Legg inn håndtering av tilfeller der man ikke får data fra Vinmonopolet. Det må passes på at stock ikke skrives til 0 bare fordi vi ikke får kontakt og data. ref. spesialslipp og queue-it

            
            # Set stock to 0 in all stores out of stock, but which has previously had it in stock
            for empty_store in empty_stores:

                # Calculate beer sale as last stock since new stock is 0
                sales = BeerStock.objects.get(beer_id=beer.beer_id,store_id=empty_store)
                self.stdout.write(f"Updated stock(=0) in store: {empty_store}. Sales {sales.product_stock}")

                obj, created = BeerStock.objects.update_or_create(
                    beer_id = beer,
                    store_id = empty_store,
                    defaults={
                    'product_stock' : 0
                    }
                )

            # Filter stock to only write stock for Molde
            for store_stock in filter(lambda x: x["name"] == str(244), stock_all_stores):
                # TODO: remove logging
                self.stdout.write(f"Updated stock(>0) in store: {store_stock['name']}")
                

                # current_store_stock = filter(lambda x: x["store_id"] == 244 ,current_stock)
                # self.stdout.write(f"Stock change: {current_store_stock['product_stock']}")

                # TODO: Add sales information

                    # update_or_create skal brukes
                obj, created = BeerStock.objects.update_or_create(
                    beer_id = beer,
                    store_id = Store.objects.get(store_id=int(store_stock["name"])),
                    defaults={
                    'product_stock' : store_stock["stockInfo"]["stockLevel"]
                    }
                )

        # Log how many new products were added to the database
        # self.stdout.write(f"Completed and inserted {new_products} new products.")

        return