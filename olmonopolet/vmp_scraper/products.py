import httpx

def get_product_details(product_id):
    '''Retrieves the main category for a product.
    
    Parameters:
    arg1 int: product_id 
    
    Returns: 
    str: Product main category
    '''

    product_url = "https://www.vinmonopolet.no/api/products/" + product_id + "/"

        
    # Get details from VMP about product
    # TODO: add try/except
    product_details = httpx.get(product_url).json()

    return product_details