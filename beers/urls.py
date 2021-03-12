from django.urls import path, include
from .views import BeerStockView, ReleaseListView, store_beers, beer_stock_search, beer_release

urlpatterns = [
    path('release/',beer_release, name='beer_release'),
    path('<int:store_id>/release',ReleaseListView.as_view(), name='release_overview'),
    path('<int:store_id>/store_beers',store_beers, name='store_beers'),
    path('<int:store_id>/beer_stock_search',beer_stock_search, name='beer_stock_search'),
    path('<int:store_id>/',BeerStockView.as_view(), name='beer_stock'),
]
