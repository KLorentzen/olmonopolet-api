from django.core.management.base import BaseCommand
from beers.models import Beer
from stock.models import BeerStock
from stores.models import Store
from sales.models import DailySale
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import beer_stock  
from olmonopolet.stock import sales 
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

class Command(BaseCommand):
    help = 'Update beer stock and daily sales from Vinmonopolet'

    def handle(self, *args, **options):
        
        # Check if Vinmonopolet is available
        if beer_stock.isVMPonline:
            self.stdout.write(f"Vinmonopolet is not available...")
            return

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
            
            # Set stock to 0 in all stores out of stock, but which has previously had it in stock
            for empty_store in empty_stores:

                # TODO: try/except dersom det ikke returneres noe (ObjectDoesNotExist)
                vmp_store = Store.objects.get(store_id=empty_store)
                current_stock = BeerStock.objects.get(beer_id=beer,store_id=vmp_store)

                obj, created = BeerStock.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    defaults={
                    'product_stock' : 0
                    }
                )
                
                daily_sales = sales.get_daily_beer_sale(
                    beer,
                    vmp_store, 
                    current_stock.product_stock, 
                    obj.product_stock
                )
                
                sale_obj, created = DailySale.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    sales_day = date.today(),
                    defaults={
                    'beers_sold': daily_sales
                    }
                )
                self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}")
                
            # Filter stock to only write stock for Molde
            for store_stock in filter(lambda x: x["name"] == str(244), stock_all_stores):
                vmp_store = Store.objects.get(store_id=int(store_stock["name"]))

                try:
                    existing_stock = BeerStock.objects.get(beer_id=beer, store_id=vmp_store)
                    # self.stdout.write(f"current stock {current_stock.product_stock} on {datetime.date.today()}")
                    current_stock = existing_stock.product_stock
                except ObjectDoesNotExist as err:
                    # Implies that beer has never been in stock before and should be 0
                    current_stock = 0

                obj, created = BeerStock.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    defaults={
                    'product_stock' : store_stock["stockInfo"]["stockLevel"]
                    }
                )
                
                daily_sales = sales.get_daily_beer_sale(
                    beer,
                    vmp_store, 
                    current_stock, 
                    obj.product_stock
                )
                
                sale_obj, created = DailySale.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    sales_day = date.today(),
                    defaults={
                    'beers_sold': daily_sales
                    }
                )
                self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}")

        return