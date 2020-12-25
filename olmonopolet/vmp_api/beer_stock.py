import httpx

def get_stock_all_stores(beer_id, vmp_session_cookie):
    '''
    Get stock for given beer in all Vinmonopolet's stores
    
    Arguments:
    arg1 int: Beer id to return stock quantity for
    arg2 obj: httpx.cookie instance from VMP including session ID
    
    Returns:
    list: List with beer stock details in all VMP stores
    '''
    URL = f"https://www.vinmonopolet.no/api/products/{beer_id}/stock"
    PARAMS = {"latitude": 0, "longitude": 0, "pageSize": 1000, "fields":'BASIC'}

    # Add exception handling
    try:
        beer_stock = httpx.get(URL, params=PARAMS, cookies=vmp_session_cookie, allow_redirects=True)

        if beer_stock.status_code != 200:
            print(f"Could not fetch stock at Vinmonopolet, got the following status code: {beer_stock.status_code}.")
            return []
        else: 
            # beer_stock.json()
            return beer_stock.json()["stores"]
    except Exception as err:
        print(f"Exception cought while requesting store stock: {err}")
        return []
