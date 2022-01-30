from django.core.management.base import BaseCommand
from beers.models import Beer
from stock.models import BeerStock, WatchList
from stores.models import Store
from sales.models import DailySale
from olmonopolet.vmp_api import beer_stock
from olmonopolet.vmp_api import utilities as vmp_utils  
from olmonopolet.stock import restock, sales 
from olmonopolet.notifications import restock as notification
from datetime import date, datetime
import httpx

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
        
        
        # Instantiate httpx Client
        with httpx.Client() as client:

            # Check if Vinmonopolet is available
            if not vmp_utils.isVMPonline(client):
                self.stdout.write(f"Vinmonopolet is not available...")
                return

            # Log when the job is executed
            start_time = datetime.now()
            self.stdout.write(f"Updating product stock @ {datetime.now()}")


            if options['watchlist']:
                # Retrieve beers in WatchList model
                beers = Beer.objects.all().exclude(watchlist = None)
            else: 
                # Retrieve all beers in database which are not added to WatchList
                beers = Beer.objects.filter(watchlist = None)

            # Retrieve all active Vinmonopolet Stores
            active_stores = Store.objects.filter(active=True).order_by('-category')


            # Update Stock for all Active Stores
            for store in active_stores:
                self.stdout.write(f"Updating stock for store: {store}")
                
                # Dictionary with key="store_id" and values are list of beers that are restocked and should be notified per email
                notify_restock = {}

                for beer in beers:

                    # Has Beer been in stock at Vinmonopolet Store - retrieve BeerStock instance
                    try:
                        current_stock = BeerStock.objects.get(beer_id=beer, store_id=store)
                    except:
                        # If stock cannot be retrieved it implies that stock
                        current_stock = False

                    # Get current stock from VMP for provided Store
                    vmp_stock = beer_stock.get_store_stock(client, beer.beer_id, store)
                    
                    # Store IDs of stores with stock > 0
                    stores_with_stock = [int(i['pointOfService']['name']) for i in vmp_stock]
                    
                    # Beer has previously been in stock but is currently not in stock
                    # Set stock to 0 in all stores out of stock, but which has previously had it in stock
                    if current_stock and store.store_id not in stores_with_stock:

                        obj, created = BeerStock.objects.update_or_create(
                            beer_id = beer,
                            store_id = store,
                            defaults={
                            'product_stock' : 0,
                            'last_product_stock' : current_stock.product_stock if current_stock.product_stock > 0 else current_stock.last_product_stock,
                            'out_of_stock_date': date.today() if current_stock.product_stock > 0 else current_stock.out_of_stock_date
                            }
                        )
                        
                        daily_sales = sales.get_daily_beer_sale(
                            beer,
                            store, 
                            current_stock.product_stock, 
                            obj.product_stock,
                            None
                        )
                        
                        sale_obj, created = DailySale.objects.update_or_create(
                            beer_id = beer,
                            store_id = store,
                            sales_day = date.today(),
                            defaults={
                            'beers_sold': daily_sales
                            }
                        )
                        self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}, store: {store}")

                    elif store.store_id in stores_with_stock:   

                        # Extract Stock response from Vinmonopolet associated with store
                        store_stock = next((filter(lambda x: x['pointOfService']['name'] in str(store.store_id), vmp_stock)))

                        if current_stock:
                            current_stock_qty = current_stock.product_stock
                            last_available_stock = current_stock.last_product_stock

                        else:
                            # Implies that beer has never been in stock before and should be 0
                            current_stock = None
                            current_stock_qty = 0
                            last_available_stock = None
                            restock_date = date.today()
                            
                        obj, created = BeerStock.objects.update_or_create(
                            beer_id = beer,
                            store_id = store,
                            defaults={
                            'product_stock' : store_stock["stockInfo"]["stockLevel"],
                            'last_product_stock' : None, 
                            'restock_qty' : restock.get_restock_qty(current_stock_qty, store_stock["stockInfo"]["stockLevel"],last_available_stock) if restock.is_restocked(current_stock_qty, store_stock["stockInfo"]["stockLevel"], last_available_stock) else current_stock.restock_qty,
                            'restock_date' : date.today() if restock.is_restocked(current_stock_qty, store_stock["stockInfo"]["stockLevel"], last_available_stock) else current_stock.restock_date,
                            'out_of_stock_date' : None,
                            'complete_restock_date' : current_stock.complete_restock_date if current_stock else restock_date
                            }
                        )
                        
                        daily_sales = sales.get_daily_beer_sale(
                            beer,
                            store, 
                            current_stock_qty, 
                            obj.product_stock,
                            last_available_stock
                        )
                        
                        sale_obj, created = DailySale.objects.update_or_create(
                            beer_id = beer,
                            store_id = store,
                            sales_day = date.today(),
                            defaults={
                            'beers_sold': daily_sales
                            }
                        )

                        # All beers that are restocked, and have been out of stock (current stock=0), for a store will be added to notification "restock"
                        # Also beers that are restocked while store stock is falsly set to 0 will be emailed as restocked
                        if restock.is_restocked(current_stock_qty, store_stock["stockInfo"]["stockLevel"], last_available_stock) and current_stock_qty == 0:
                            notify_restock.setdefault(store,[]).append(beer)

                            # Update date and restock quantity when stock was completely re-stocked for given beer
                            obj, created = BeerStock.objects.update_or_create(
                            beer_id = beer,
                            store_id = store,
                            defaults={
                                'restock_qty' : store_stock["stockInfo"]["stockLevel"],
                                'complete_restock_date' : date.today(),
                            }
                        )

                        self.stdout.write(f"Updated {obj.beer_id.name}, stock: {obj.product_stock}, sales: {sale_obj.beers_sold}, store: {store}")
            
            
                # Send email notification for Beers that are restocked
                if len(notify_restock) > 0:
                    notification.send_restock_email(notify_restock)
                    self.stdout.write(f"notification: {notify_restock}")

        end_time = datetime.now()
        self.stdout.write(f"Product stock update took {end_time - start_time} seconds")

        return