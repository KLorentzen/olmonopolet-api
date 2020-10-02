class RestockError(Exception):
    '''
    Raised when restock is not possible
    '''
    pass
    def __init__(self, message):
        self.message = message

def is_restocked(current_stock, new_stock, stock_before_empty):
    """
    Check if a Beer has been re-stocked based on current, stock before empty and new stock status.
    If the restock quantity is equal to the stock prior to stock=0 it is not considered to be a restock. 
    Such case represent a bug in the VMP system where beers get stock=0 and then is reset.      

    Parameters:  
    int: current product stock  
    int: New product stock  
    int: Last available product stock before store was empty  

    Returns:  
    bool: True/False if beer is restocked  
    """

    if stock_before_empty and new_stock == stock_before_empty:
        return False
    elif new_stock > current_stock:
        return True
    else:
        return False

def get_restock_qty(current_stock, new_stock):
    '''
    Return the re-stock quantity for beer.  

    Parameters:  
    int: current product stock  
    int: New product stock  

    Returns:  
    int: Restock quantity  
    '''
    _restock_qty = new_stock-current_stock

    if _restock_qty <= 0:
        raise RestockError('Trying to restock when new stock is <= current stock. This is not a restock!')
    
    return _restock_qty