from django.core.management.base import BaseCommand
from beers.models import Product, Beer
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import products as vmp_api_products 
from olmonopolet.vmp_scraper import products as vmp_scraper_products 

class Command(BaseCommand):
    help = 'Update products from Vinmonopolet'

    def handle(self, *args, **options):
        # Used for logging
        new_products = 0
        
        # Get list of all products in database
        db_products = list(Product.objects.values_list('product_id', flat=True))

        # Retrieves all VMP products currently in stock
        all_products = vmp_api_products.get_all_products()

        for product in all_products:

            # Only add the product if not already in the database
            if int(product["productId"]) in db_products:
                pass
            else:
                # Get product details from Vinmonopolet
                product_details = vmp_scraper_products.get_product_details(product["productId"])

                new_obj = Product.objects.create(
                    product_id = product["productId"],
                    main_category = product_details["main_category"]["code"] 
                    )

                # Add all products that are 'øl' to the Beer table
                if product_details["main_category"]["code"] == 'øl':
                    try:
                        
                        beer_obj = Beer.objects.create(
                            beer_id = product["productId"] ,
                            name = product_details["name"],
                            # brewery = '',
                            # style = '',
                            # alc_volume = '',
                            volume = product_details["volume"]["value"],
                            selection = product_details["product_selection"],
                            url = product_details["url"])
                    except NameError as err:
                        self.stdout.write(f"Could not insert beer: {product['productId']}")
                        self.stdout.write(err)
                
                new_products += 1

        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_products} new products.")

        return