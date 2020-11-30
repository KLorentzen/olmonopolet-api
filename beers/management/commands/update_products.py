from django.core.management.base import BaseCommand
from beers.models import Product, Beer
from untappd.models import UntappdMapping
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import products as vmp_api_products 
from olmonopolet.vmp_scraper import product_details as vmp_details
from olmonopolet.untappd_scraper import mapping 
from datetime import datetime

class Command(BaseCommand):
    help = '''
    Update database with products from Vinmonopolet

    1. Gets all products currently in stock at Vinmonopolet from products/GET accumulated-stock
    2. Add new products to database
    3. Check which products are of given category and add them to Beer model.
        - categories: [øl, mjød]
    4. Map beer name from Vinmonopolet with beer at Untappd.com. If mapping is obtained it will be written to the UntappdMapping model.
    
    '''

    def handle(self, *args, **options):
        # Log when the job is executed
        self.stdout.write(f"Updating Vinmonopolet products @ {datetime.now()}")

        # TODO: Add functionality to log to file
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
                product_details = vmp_api_products.get_product_details(product["productId"])

                if not product_details:
                    self.stdout.write("Could not connect with Vinmonopolet")
                    break

                # Add product to Product table
                new_prod_obj = Product.objects.create(
                    product_id = product["productId"],
                    main_category = product_details["main_category"]["code"] 
                    )

                # Add all products that are 'øl' to the Beer table
                if product_details["main_category"]["code"] in ['øl', 'mjød']:
                    try:
                        
                        # Get Additional details about the beer from the Web Page
                        # TODO: Deprecated after URL with full product details were found
                        # product_web_details = vmp_details.get_details_web(product_details["url"])
                        
                        beer_obj = Beer.objects.create(
                            beer_id = new_prod_obj ,
                            name = product_details["name"],
                            brewery = product_details['main_producer']['name'],
                            country = product_details["main_country"]["code"],
                            style = product_details['main_sub_category']['name'] if "main_sub_category" in product_details else None,
                            price = product_details["price"]["value"],
                            alc_volume = product_details['alcohol']['value'],
                            volume = product_details["volume"]["value"],
                            selection = product_details["product_selection"] if "product_selection" in product_details else None,
                            url = 'https://www.vinmonopolet.no' + product_details["url"],
                            status = product_details["status"],
                            buyable = product_details["buyable"],
                            launch_date = datetime.strptime(product_details["expiredDate"],"%Y-%m-%d") 
                            ),

                    except Exception as err:
                        self.stdout.write(f"Could not insert beer: {product['productId']}")
                        self.stdout.write(err)
                
                new_products += 1

        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_products} new products.")

        return