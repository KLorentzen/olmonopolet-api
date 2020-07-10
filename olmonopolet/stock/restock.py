class RestockError(Exception):
    '''
    Raised when restock is not possible
    '''
    pass
    def __init__(self, message):
        self.message = message

def is_restocked(current_stock, new_stock):
    """
    Check if a Beer has been re-stocked based on current and new stock status    

    Parameters:  
    int: current product stock  
    int: New product stock  

    Returns:  
    bool: True/False if beer is restocked  
    """

    if new_stock > current_stock:
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