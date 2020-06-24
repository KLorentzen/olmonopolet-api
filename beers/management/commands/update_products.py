from django.core.management.base import BaseCommand
from beers.models import Product, Beer
from untappd.models import UntappdMapping
from django.db.utils import IntegrityError
from olmonopolet.vmp_api import products as vmp_api_products 
from olmonopolet.vmp_scraper import product_details as vmp_details
from olmonopolet.untappd_scraper import mapping 

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
                        product_web_details = vmp_details.get_details_web(product_details["url"])
                        
                        beer_obj = Beer.objects.create(
                            beer_id = new_prod_obj ,
                            name = product_details["name"],
                            brewery = product_web_details['brewery'],
                            country = product_details["main_country"]["code"],
                            style = product_web_details['style'],
                            price = product_details["price"]["value"],
                            alc_volume = product_web_details['alcohol'],
                            volume = product_details["volume"]["value"],
                            selection = product_details["product_selection"],
                            url = product_details["url"])

                        # Map Beer from VMP with Untappd
                        untappd_mapping = mapping.find_untappd_mapping(beer_obj.name)
                        mapping_obj = UntappdMapping.objects.create(
                            beer_id = beer_obj,
                            untappd_id = untappd_mapping['id'],
                            name = untappd_mapping['name'],
                            url = untappd_mapping['url']
                        )

                    except Exception as err:
                        self.stdout.write(f"Could not insert beer: {product['productId']}")
                        self.stdout.write(err)
                
                new_products += 1

        # Log how many new products were added to the database
        self.stdout.write(f"Completed and inserted {new_products} new products.")

        return