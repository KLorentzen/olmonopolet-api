from sales.models import DailySale
from stores.models import Store
from beers.models import Beer
from olmonopolet.stock import restock
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def get_daily_beer_sale(beer, store, current_stock, new_stock, stock_before_empty):
    """
    Get accumulated sales for a beer in a store, based on stock diff for today. 
    Checks current sales for the day and adds stock diff to sales if new stock is less than current stock.
    Checks that new stock is different from stock before store was empty since this represent a bug in the VMP system where beers get stock=0 and then is reset.  
    Returns negative sales when VMP has set stock to 0 and then reset to stock before zero.

    Parameters:  
    Beer model instance:  
    Store model instance:  
    int: current stock in DB before updated with new stock  
    int: new stock  
    int: Last available product stock before store was empty  

    Returns:  
    int: Sum of daily sales in store for beer.   
    """

    try:
        # TODO: Vurdere om det må gjøres noen spesielle hensyn ved overgang mellom dager?!
        # Get current sales for today, if there are any
        sales_today = DailySale.objects.get(
            beer_id=beer, store_id=store, sales_day=date.today()
        )
        accumulated_daily_sale = sales_today.beers_sold
    except ObjectDoesNotExist as err:
        # First stock/sales update of each date will be processed here
        accumulated_daily_sale = 0

    if new_stock > current_stock and not restock.is_restocked(current_stock,new_stock, stock_before_empty):
        # Subtract sales that were falsly assigned due to VMP setting stock to 0 and then resetting stock
        accumulated_daily_sale -= stock_before_empty
    elif new_stock > current_stock:
        # Re-stock implies no additional sales
        pass
    elif new_stock <= current_stock:
        accumulated_daily_sale += current_stock - new_stock


    return accumulated_daily_sale
