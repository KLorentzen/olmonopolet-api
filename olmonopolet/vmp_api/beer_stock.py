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
    try:
        beer_stock = httpx.get(URL,params=PARAMS, allow_redirects=True)

        if beer_stock.status_code != 200:
            print(f"Could not fetch stock at Vinmonopolet, got the following status code: {beer_stock.status_code}.")
            return []
        else: 
            # beer_stock.json()
            return beer_stock.json()["stores"]
    except Exception as err:
        print(f"Exception cought: {err}")
        return []

def isVMPonline():
    '''
    Check if vinmonopolet is available for queries.  
    On days with product releases at Vinmonopolet you will be redirected to a queue, hence it will not be possible to fetch data.  
    
    Arguments:  
    none  
      
    Returns:  
    bool: Vinmonopolet availability
    '''

    URL = "https://www.vinmonopolet.no/"

    try:
        response = httpx.get(URL, allow_redirects=False)
        if response.status_code != 200:
            return False
        else:
            return True
    except Exception as err:
        return False