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


def get_products(selection, page, vmp_session_cookie):
    '''Retrieve products, for a selection, that are currently in stock by Vinmonopolet.  
    Each page retrieved returns 100 products
    
    Parameters:
    arg1 str: product selection, i.e. 'øl', 'mjød', 'sider'  
    arg2 int: page number to retrieve as results from VMP are paginated
      
    Returns:  
    int: HTTP status code from VMP request  
    list: Products on current page  
    int: Total number of pages with products for current selection
    '''

    URL = 'https://www.vinmonopolet.no/api/search?q=:relevance:visibleInSearch:true:mainCategory:%C3%B8l&searchType=product&fields=FULL&pageSize=24&currentPage=0'
    PARAMS = {'q':f':relevance:visibleInSearch:true:mainCategory:{selection}',
               'searchType': 'product',
               'fields': 'FULL',
               'pageSize': 100,
               'currentPage': page}
    
    try:
        response = httpx.get(URL, params=PARAMS, cookies=vmp_session_cookie)
        response_code = response.status_code
        content = response.json()
        products = content['productSearchResult']['products']
        total_pages = content['productSearchResult']['pagination']['totalPages']
        total_products = content['productSearchResult']['pagination']['totalResults']
    except Exception as err:
        response_code = 500
        products = []
        total_pages = 0
    
    return response_code, products, total_pages

def get_product_details(product_id, vmp_session_cookie):
    '''Retrieve product details.

    Parameters:
    arg1 int: product_id 
    arg2 obj: httpx.cookie instance from VMP including session ID

    Returns: 
    dict: JSON with product details if success, otherwise returns False (bool).
    '''
    product_url = f"https://www.vinmonopolet.no/api/products/{product_id}" #+ product_id 
    PARAMS = {"fields": 'FULL'}

    # Get details from VMP about product
    try:
        product_details = httpx.get(product_url,params=PARAMS, cookies=vmp_session_cookie).json()
    except Exception as err:
        product_details = False

    return product_details