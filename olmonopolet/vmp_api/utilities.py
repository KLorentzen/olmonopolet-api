import httpx


def isVMPonline(client):
    '''
    Check if vinmonopolet is available for queries.  
    On days with product releases at Vinmonopolet you will be redirected to a queue, hence it will not be possible to fetch data.  
    
    Arguments:  
    arg1 obj: httpx Client instance  
      
    Returns:  
    bool: Vinmonopolet availability
    '''

    URL = "https://www.vinmonopolet.no/"
    HEADERS = {
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0)'
    }

    try:
        response = client.get(URL, headers=HEADERS)
        
        # Check if actual url matches requested url
        if response.url != URL:
            return False
        else:
            return True
    except Exception as err:
        return False

def get_VMP_cookies():
    '''
    !!!!DEPRECATED!!!!
    Query Vinmonopolet in order to initialise cookies from the site. 
    Such cookies are required when requesting resources from certain VMP endpoints.  

    Returns:  
    httpx.cookie instance
    '''
    URL = "https://www.vinmonopolet.no/"
    HEADERS = {
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0)'
    }

    try:
        vmp = httpx.get(URL, headers=HEADERS)

        return vmp.cookies
    except Exception as err:
        print(f"Exception cought while requesting VMP cookies: {err}")
        return 