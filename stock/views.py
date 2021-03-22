from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Max
from rest_framework import generics
from .models import BeerStock
from beers.models import Beer
from stores.models import Store
from .serializers import BeerStockSerializer
from django.views.generic import TemplateView
from datetime import datetime, timedelta


# View Functions
def stock_change_in(request, store_id):
    '''
    Return all beers that were restocked for given Vinmonopol
    Paginated in order to use infinite scroll
    '''
    queryset = BeerStock.objects.filter(store_id=store_id).order_by('-complete_restock_date', 'beer_id__name')

    paginator = Paginator(queryset, 75, 0)

    page_number = request.GET.get('page')
    stock_change = paginator.get_page(page_number)
    
    return render(request, 'stubs/beer_stock_change_in.html', {'stock_change': stock_change, 'store_id': store_id})

def stock_change_out(request, store_id):
    '''
    Return all beers that went out of stock for given Vinmonopol
    Paginated in order to use infinite scroll
    '''
    queryset = BeerStock.objects.filter(out_of_stock_date__isnull=False).filter(store_id=store_id).order_by('-out_of_stock_date', 'beer_id__name')

    paginator = Paginator(queryset, 75, 0)

    page_number = request.GET.get('page')
    stock_change = paginator.get_page(page_number)
    
    return render(request, 'stubs/beer_stock_change_out.html', {'stock_change': stock_change, 'store_id': store_id})

# Regular Views
class StockChangeTemplateView(TemplateView):
    template_name = 'stock_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        context['last_updated'] = BeerStock.objects.filter(store_id=self.kwargs['store_id']).aggregate(Max('last_updated'))['last_updated__max']
        return context

# API Views
class BeerStockListAPIView(generics.ListAPIView):
    queryset = BeerStock.objects.all()
    serializer_class = BeerStockSerializer
    filterset_fields = ['store_id', 'beer_id']