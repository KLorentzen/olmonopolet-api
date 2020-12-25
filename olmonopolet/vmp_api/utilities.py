import httpx


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

def get_VMP_cookies():
    '''
    Query Vinmonopolet in order to initialise cookies from the site. 
    Such cookies are required when requesting resources from certain VMP endpoints.  

    Returns:  
    httpx.cookie instance
    '''
    URL = "https://www.vinmonopolet.no/"

    try:
        vmp = httpx.get(URL)

        return vmp.cookies
    except Exception as err:
        print(f"Exception cought while requesting VMP cookies: {err}")
        return 