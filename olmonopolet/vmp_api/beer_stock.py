import httpx

def get_store_stock(client, beer_id, store):
    '''
    Get stock for given beer in a Vinmonopole store  
    
    Arguments:  
    arg1 obj: httpx Client instance  
    arg2 int: Beer id to return stock quantity for   
    arg3 obj: Store model instance  
    
    Returns:  
    list: List with beer stock details in all VMP stores  
    '''
    URL = f"https://www.vinmonopolet.no/api/products/{beer_id}/stock"
    PARAMS = {"latitude": store.latitude, "longitude": store.longitude, "pageSize": 10, "fields":'BASIC'}
    HEADERS = {
        # 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0)'
    }
    
    try:
        beer_stock = client.get(URL, params=PARAMS, headers=HEADERS, allow_redirects=True)

        if beer_stock.status_code != 200:
            print(f"Could not fetch stock at Vinmonopolet, got the following status code: {beer_stock.status_code}.")
            return []
        else: 
            # beer_stock.json()
            return beer_stock.json()["stores"]
    except Exception as err:
        print(f"Exception cought while requesting store stock: {err}")
        return []
