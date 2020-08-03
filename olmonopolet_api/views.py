from django.shortcuts import render
from stock.models import BeerStock
from stores.models import Store


def frontend(request):
    '''
    Entrypoint for Vue JS Application
    '''

    stock_info = BeerStock.objects.all()
    stores = Store.objects.all()

    context_data = {
        'beer_stock': stock_info,
        'stores': stores
    }

    return render(request,'frontend/index.html', context_data)