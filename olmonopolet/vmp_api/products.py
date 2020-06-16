import os, httpx

def get_all_products():
    '''Retrieve all products that are currently in stock by Vinmonopolet. Uses "products/GET accumulated-stock" API endpoint from VMP.
    
    Parameters:
    none

    Returns: 
    list: List of all products currently in stock at Vinmonopolet in JSON format
    '''

    URL = "https://apis.vinmonopolet.no/products/v0/accumulated-stock"
    HEADERS = {"Ocp-Apim-Subscription-Key": os.environ.get('VMP_PRIMARY_KEY') }
    PARAMS = {"maxResults": 100000}

    # Retrieve all products currently in stock at VMP
    all_products = httpx.get(URL,headers=HEADERS,params=PARAMS).json()
    # TODO: Add try/except for api-call

    # TODO: Return all products
    # For testing purposes only the last 100 products will be returned
    return all_products[-100:]


    def get_product_details(product_id):
    '''Retrieve product details.
    
    Parameters:
    arg1 int: product_id 
    
    Returns: 
    str: JSON with product details
    '''
    product_url = "https://www.vinmonopolet.no/api/products/" + product_id + "/"

    # Get details from VMP about product
    # TODO: add try/except
    product_details = httpx.get(product_url).json()

    return product_details