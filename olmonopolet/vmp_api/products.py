import os, httpx

def get_all_products():
    '''Retrieve all products that are currently in stock by Vinmonopolet. Uses "GET accumulated-stock" API endpoint from VMP.
    
    Parameters:
    none

    Returns: 
    list: List of all products currently in stock at Vinmonopolet
    '''

    URL = "https://apis.vinmonopolet.no/products/v0/accumulated-stock"
    HEADERS = {"Ocp-Apim-Subscription-Key": os.environ.get('VMP_PRIMARY_KEY') }
    PARAMS = {"maxResults": 100000}

    # Retrieve all products currently in stock at VMP
    all_products = httpx.get(URL,headers=HEADERS,params=PARAMS).json()
    # TODO: Add try/except for api-call

    # TODO: Return all products
    # For testing purposes only the last 20 products will be returned
    return all_products[-100:]