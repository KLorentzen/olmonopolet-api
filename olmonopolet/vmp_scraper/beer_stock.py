import httpx

def get_stock_all_stores(beer_id):
    '''
    Get stock for given beer in all Vinmonopolet's stores
    
    Arguments:
    arg1 int: Beer id to return stock quantity for
    
    Returns:
    list: List with beer stock details in all VMP stores
    '''
    
    URL = f"https://www.vinmonopolet.no/api/products/{beer_id}/stock"
    PARAMS = {"latitude": 0, "longitude": 0, "pageSize": 1000}

    # Add exception handling
    beer_stock = httpx.get(URL,params=PARAMS).json()
    
    return beer_stock["stores"]
