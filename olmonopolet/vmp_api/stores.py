import httpx
import os

def get_all_stores():
    '''
    Retrieve Vinmonopolet stores. Uses GET store details API from VMP.

    Parameters:
    none
    
    Returns:
    list: List with all Vinmonopolet stores in JSON format
    '''

    URL = "https://apis.vinmonopolet.no/stores/v0/details"
    HEADERS = {"Ocp-Apim-Subscription-Key": os.environ.get('VMP_PRIMARY_KEY')}

    try:
        all_stores = httpx.get(URL, headers=HEADERS).json()
        return all_stores
    except Exception as err:
        print(err)