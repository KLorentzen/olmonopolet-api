from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Beer
from stores.models import Store
from .serializers import BeerSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from django.db.models import F, Q, OuterRef, Subquery
from django.utils import timezone
from untappd.models import UserCheckIn

# Create your views here.

# View Functions
def store_beers(request, store_id):
    '''
    Returns all beers in stock at given Vinmonopolet store
    Paginated in order to use infinite scroll
    '''
    
    queryset = Beer.objects.filter(beerstock__product_stock__gt=0, beerstock__store_id=store_id).order_by(F('untappd__rating').desc(nulls_last=True))
    
    if request.user.is_authenticated:
        
        # This subquery returns the rating of any beers the User has checked in to Untappd
        check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'),user_id=request.user)
        queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))

    paginator = Paginator(queryset, 50, 0)

    page_number = request.GET.get('page')
    beers = paginator.get_page(page_number)

    return render(request, 'stubs/store_inventory.html', {'beers': beers, 'store_id': store_id, 'full_store_stock':True})

def beer_stock_search(request, store_id):
    '''
    Used by search bar in beer stock page (beer_stock)
    Returns a list of all matched beers in stock at given Vinmonopolet store
    PS: Search results are not paginated
    '''

    # Check if query is empty
    if request.POST["query"] != '':
        # Fetch all Beers in stock at store 
        queryset = Beer.objects.filter(beerstock__product_stock__gt=0, beerstock__store_id=store_id).order_by(F('untappd__rating').desc(nulls_last=True))
        # Find beers that match 'query' by name or brewery 
        queryset = queryset.filter(Q(name__icontains=request.POST["query"]) | Q(brewery__icontains=request.POST["query"]))
        
        if request.user.is_authenticated:
            # This subquery returns the rating of any beers the User has checked in to Untappd
            check_in_subquery = UserCheckIn.objects.filter(beer_id = OuterRef('beer_id'),user_id=request.user)
            queryset = queryset.annotate(untappd_rating=Subquery(check_in_subquery.values('rating')[:1]))

    else:
        # Returns all beers in stock if query string is empty ('')
        return redirect('store_beers', store_id)
    return render(request, 'stubs/store_inventory.html', {'beers': queryset, 'store_id': store_id, 'search':True})

def beer_release(request):
    '''
    Return all beers which are to be released/launched in the future
    Paginated in order to use infinite scroll
    '''
    queryset = Beer.objects.filter(launch_date__gte=timezone.now()).order_by('launch_date', 'selection', 'name')
    paginator = Paginator(queryset, 50, 0)

    page_number = request.GET.get('page')
    beers = paginator.get_page(page_number)

    return render(request, 'stubs/beer_release.html', {'beers': beers})

# Regular Views
class BeerStockView(TemplateView):
    template_name = "beer_stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        return context

class ReleaseListView(TemplateView):
    template_name = "release.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        return context


# API Views
class BeerList(generics.ListAPIView):
    queryset=Beer.objects.all()
    serializer_class=BeerSerializer

class BeerDetail(generics.RetrieveAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
