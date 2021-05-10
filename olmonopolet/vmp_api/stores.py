import httpx
import os

def get_all_stores(client):
    '''
    Retrieve Vinmonopolet stores. Uses GET store details API from VMP.

    Parameters:
    arg1 obj: httpx Client instance  
    
    Returns:
    list: List with all Vinmonopolet stores in JSON format
    '''

    URL = "https://apis.vinmonopolet.no/stores/v0/details"
    HEADERS = {"Ocp-Apim-Subscription-Key": os.environ.get('VMP_PRIMARY_KEY'),
                'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0)'}

    try:
        all_stores = client.get(URL, headers=HEADERS).json()
        return all_stores
    except Exception as err:
        print(err)