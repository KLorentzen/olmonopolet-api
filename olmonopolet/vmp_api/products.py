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
    try:
        all_products = httpx.get(URL,headers=HEADERS,params=PARAMS).json()
    except Exception as err:
        all_products = []

    # For testing purposes change this return value to all_products[:X] to slice list
    return all_products


def get_product_details(product_id):
    '''Retrieve product details.

    Parameters:
    arg1 int: product_id 

    Returns: 
    dict: JSON with product details if success, otherwise returns False (bool).
    '''
    product_url = "https://www.vinmonopolet.no/api/products/" + product_id 
    PARAMS = {"fields": 'FULL'}

    # Get details from VMP about product
    try:
        product_details = httpx.get(product_url,params=PARAMS).json()
    except Exception as err:
        product_details = False

    return product_details