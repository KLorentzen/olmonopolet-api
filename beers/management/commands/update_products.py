from django.core.management.base import BaseCommand
from beers.models import Product, Beer
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import products as vmp_api_products 
from olmonopolet.vmp_scraper import product_details as vmp_details
from olmonopolet.vmp_api import utilities as vmp_utils  
from datetime import datetime

class Command(BaseCommand):
    help = '''
    Update database with products from Vinmonopolet

    1. Gets all products currently in stock at Vinmonopolet from URL with JSON response
    2. Add new products to database
    3. Check which products are of given category and add them to Beer model.
        - categories: [øl, mjød, sider]
    
    '''

    def handle(self, *args, **options):
        # Log when the job is executed
        self.stdout.write(f"Updating Vinmonopolet products @ {datetime.now()}")

        new_products = 0
        
        # Get list of all products in database
        db_products = list(Product.objects.values_list('product_id', flat=True))

        # Obtain session ID from VMP
        vmp_session_cookie = vmp_utils.get_VMP_cookies()

        # Retrieves all products currently in stock
        product_types = ['øl', 'mjød', 'sider']
        all_products = []

        for product_type in product_types:
            page = 0
            while True:
                HTTP_CODE, products, total_page_count = vmp_api_products.get_products(product_type, page, vmp_session_cookie)
                page += 1
                all_products.extend(products)

                if page > total_page_count:
                    break

        for product in all_products:

            # Only add the product if not already in the database
            if int(product["code"]) in db_products:
                pass
            else:
                # Get product details from Vinmonopolet
                product_details = vmp_api_products.get_product_details(product["code"], vmp_session_cookie)

                if not product_details:
                    self.stdout.write("Could not connect with Vinmonopolet")
                    break

                # Add product to Product table
                new_prod_obj = Product.objects.create(
                    product_id = product["code"],
                    main_category = product["main_category"]["name"].lower() 
                    )

                # Add all products to the Beer table
                try:
                    
                    beer_obj = Beer.objects.create(
                        beer_id = new_prod_obj ,
                        name = product["name"],
                        brewery = product_details['main_producer']['name'],
                        country = product["main_country"]["name"],
                        style = product_details['main_sub_category']['name'] if "main_sub_category" in product_details else None,
                        price = product["price"]["value"],
                        alc_volume = product_details['alcohol']['value'],
                        volume = product["volume"]["value"],
                        selection = product["product_selection"] if "product_selection" in product_details else None,
                        url = 'https://www.vinmonopolet.no' + product["url"],
                        status = product["status"],
                        buyable = product["buyable"],
                        launch_date = datetime.strptime(product_details["expiredDate"],"%Y-%m-%d") 
                        ),

                except Exception as err:
                    self.stdout.write(f"Could not insert beer: {new_prod_obj}")
                    self.stdout.write(err)
                
                new_products += 1

        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_products} new products.")

        return