from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import F, Q, Max, OuterRef, Subquery
from rest_framework import generics
from .models import BeerStock
from beers.models import Beer
from stores.models import Store
from .serializers import BeerStockSerializer
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from untappd.models import UserCheckIn, UserWishList


# View Functions
def store_beers(request, store_id):
    '''
    Returns all beers in stock at given Vinmonopolet store
    Paginated in order to use infinite scroll
    '''
    
    queryset = BeerStock.objects.filter(product_stock__gt=0, store_id=store_id).order_by(F('beer_id__untappd__rating').desc(nulls_last=True))
    
    if request.user.is_authenticated:
        
        # This subquery returns the rating of any beers the User has checked in to Untappd
        check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'), user_id=request.user)
        queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))
        
        # This subquery returns a value if User has the Beer in Wish List on Untappd
        wishlist_subquery = UserWishList.objects.filter(beer_id = OuterRef('beer_id'), user_id=request.user)
        queryset = queryset.annotate(untappd_wishlist=Subquery(wishlist_subquery.values('user')[:1]))

    paginator = Paginator(queryset, 50, 0)

    page_number = request.GET.get('page')
    beerstock = paginator.get_page(page_number)

    return render(request, 'stubs/store_inventory.html', {'beerstock': beerstock, 'store_id': store_id, 'full_store_stock':True})

def beer_stock_search(request, store_id):
    '''
    Used by search bar in beer stock page (beer_stock)
    Returns a list of all matched beers in stock at given Vinmonopolet store
    PS: Search results are not paginated
    '''

    # Check if query is empty
    if request.POST["query"] != '':
        # Fetch all Beers in stock at store 
        queryset = BeerStock.objects.filter(product_stock__gt=0, store_id=store_id).order_by(F('beer_id__untappd__rating').desc(nulls_last=True))
        # Find beers that match 'query' by name or brewery 
        queryset = queryset.filter(Q(beer_id__name__icontains=request.POST["query"]) | Q(beer_id__brewery__icontains=request.POST["query"]))
        
        if request.user.is_authenticated:
            # This subquery returns the rating of any beers the User has checked in to Untappd
            check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'),user_id=request.user)
            queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))

            # This subquery returns a value if User has the Beer in Wish List on Untappd
            wishlist_subquery = UserWishList.objects.filter(beer_id = OuterRef('beer_id'), user_id=request.user)
            queryset = queryset.annotate(untappd_wishlist=Subquery(wishlist_subquery.values('user')[:1]))

    else:
        # Returns all beers in stock if query string is empty ('')
        return redirect('store_beers', store_id)
    return render(request, 'stubs/store_inventory.html', {'beerstock': queryset, 'store_id': store_id, 'search':True, 'query':request.POST["query"]})

def stock_change_in(request, store_id):
    '''
    Return all beers that were restocked for given Vinmonopol
    Paginated in order to use infinite scroll
    '''
    queryset = BeerStock.objects.filter(store_id=store_id).order_by('-complete_restock_date', 'beer_id__name')

    if request.user.is_authenticated:
        # This subquery returns the rating of any beers the User has checked in to Untappd
        check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'),user_id=request.user)
        queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))

        # This subquery returns a value if User has the Beer in Wish List on Untappd
        wishlist_subquery = UserWishList.objects.filter(beer_id = OuterRef('beer_id'), user_id=request.user)
        queryset = queryset.annotate(untappd_wishlist=Subquery(wishlist_subquery.values('user')[:1]))

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

    if request.user.is_authenticated:
        # This subquery returns the rating of any beers the User has checked in to Untappd
        check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'),user_id=request.user)
        queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))

        # This subquery returns a value if User has the Beer in Wish List on Untappd
        wishlist_subquery = UserWishList.objects.filter(beer_id = OuterRef('beer_id'), user_id=request.user)
        queryset = queryset.annotate(untappd_wishlist=Subquery(wishlist_subquery.values('user')[:1]))
        
    paginator = Paginator(queryset, 75, 0)

    page_number = request.GET.get('page')
    stock_change = paginator.get_page(page_number)
    
    return render(request, 'stubs/beer_stock_change_out.html', {'stock_change': stock_change, 'store_id': store_id})

# Regular Views
class BeerStockView(TemplateView):
    template_name = "beer_stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        return context

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