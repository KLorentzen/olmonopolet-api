from django.urls import path, include
from .views import StockChangeTemplateView, stock_change_in, stock_change_out, BeerStockView, store_beers, beer_stock_search

urlpatterns = [
    path('changes/<int:store_id>/in/', stock_change_in, name='stock_change_in'),
    path('changes/<int:store_id>/out/', stock_change_out, name='stock_change_out'),
    path('changes/<int:store_id>/', StockChangeTemplateView.as_view(), name='stock_change'),
    path('<int:store_id>/store_beers', store_beers, name='store_beers'),
    path('<int:store_id>/beer_stock_search', beer_stock_search, name='beer_stock_search'),
    path('<int:store_id>/', BeerStockView.as_view(), name='beer_stock'),
]
