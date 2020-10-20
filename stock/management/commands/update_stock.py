from django.core.management.base import BaseCommand
from beers.models import Beer
from stock.models import BeerStock, WatchList
from stores.models import Store
from sales.models import DailySale
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import beer_stock  
from olmonopolet.stock import restock, sales 
from olmonopolet.notifications import restock as notification
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime

class Command(BaseCommand):
    help = '''Update beer stock and daily sales from Vinmonopolet.  
    Stock for all products fetched by default.  
    Use option --watchlist for stock update of Watchlist items'''

    
    def add_arguments(self, parser):
        parser.add_argument(
            '--watchlist',
            action='store_true',
            help='Update stock for items listen in stock.Watchlist',
        )

    def handle(self, *args, **options):
        
        # Check if Vinmonopolet is available
        # TODO: Improve check such that stock is not set to 0 on days with Queue or when stock is set to 0 and set back to the old stock again
        if not beer_stock.isVMPonline:
            self.stdout.write(f"Vinmonopolet is not available...")
            return

        # Log when the job is executed
        start_time = datetime.now()
        self.stdout.write(f"Updating product stock @ {datetime.now()}")

        # Dictionary with key="store_id" and values are list of beers that are restocked and should be notified per email
        notify_restock = {}

        if options['watchlist']:
            # Retrieve beers in WatchList model
            beers = Beer.objects.all().exclude(watchlist = None)
        else: 
            # Retrieve all beers in database which are not added to WatchList
            beers = Beer.objects.filter(watchlist = None)
            # beers = Beer.objects.filter(name__contains='Kveldsbris') | Beer.objects.filter(name__contains='Lervig')

        for beer in beers:

            # Get Stores which have had the beer in stock at some point
            old_stock = BeerStock.objects.filter(beer_id=beer).values_list("store_id",flat=True)
            
            # Get current stock from VMP
            stock_all_stores = beer_stock.get_stock_all_stores(beer.beer_id)
            
            # Store IDs of stores with stock > 0
            stores_with_stock = [int(i['name']) for i in stock_all_stores]

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
                    'product_stock' : 0,
                    'last_product_stock' : current_stock.product_stock if current_stock.product_stock > 0 else None,
                    'out_of_stock_date': date.today() if current_stock.product_stock > 0 else current_stock.out_of_stock_date
                    }
                )
                
                daily_sales = sales.get_daily_beer_sale(
                    beer,
                    vmp_store, 
                    current_stock.product_stock, 
                    obj.product_stock,
                    None
                )
                
                sale_obj, created = DailySale.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    sales_day = date.today(),
                    defaults={
                    'beers_sold': daily_sales
                    }
                )
                self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}, store: {vmp_store}")
                
            # Filter stock to only write stock for Molde/Egersund
            for store_stock in filter(lambda x: x["name"] in [str(244),str(209)], stock_all_stores):
                vmp_store = Store.objects.get(store_id=int(store_stock["name"]))

                try:
                    existing_stock = BeerStock.objects.get(beer_id=beer, store_id=vmp_store)
                    # self.stdout.write(f"current stock {current_stock.product_stock} on {datetime.date.today()}")
                    current_stock = existing_stock.product_stock
                    last_available_stock = existing_stock.last_product_stock
                except ObjectDoesNotExist as err:
                    # Implies that beer has never been in stock before and should be 0
                    current_stock = 0
                    last_available_stock = None
                    
                obj, created = BeerStock.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    defaults={
                    'product_stock' : store_stock["stockInfo"]["stockLevel"],
                    'last_product_stock' : None, 
                    'restock_qty' : restock.get_restock_qty(current_stock, store_stock["stockInfo"]["stockLevel"]) if restock.is_restocked(current_stock, store_stock["stockInfo"]["stockLevel"], last_available_stock) else existing_stock.restock_qty,
                    'restock_date' : date.today() if restock.is_restocked(current_stock, store_stock["stockInfo"]["stockLevel"], last_available_stock) else existing_stock.restock_date,
                    'out_of_stock_date' : None
                    }
                )
                
                daily_sales = sales.get_daily_beer_sale(
                    beer,
                    vmp_store, 
                    current_stock, 
                    obj.product_stock,
                    last_available_stock
                )
                
                sale_obj, created = DailySale.objects.update_or_create(
                    beer_id = beer,
                    store_id = vmp_store,
                    sales_day = date.today(),
                    defaults={
                    'beers_sold': daily_sales
                    }
                )

                # All beers that are restocked, and have been out of stock (current stock=0), for a store will be added to notification "restock"
                if restock.is_restocked(current_stock, store_stock["stockInfo"]["stockLevel"], last_available_stock) and current_stock == 0:
                    notify_restock.setdefault(vmp_store,[]).append(beer)

                self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}, store: {vmp_store}")
        
        
        # Send email notification for Beers that are restocked
        if len(notify_restock) > 0:
            notification.send_restock_email(notify_restock)

        end_time = datetime.now()
        self.stdout.write(f"Product stock update took {end_time - start_time} seconds")

        self.stdout.write(f"notification: {notify_restock}")
        return