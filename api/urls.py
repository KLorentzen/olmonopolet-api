from django.urls import path, include

urlpatterns = [
    path('beers/',include('beers.urls')),
    path("stores/", include('stores.urls')),
    path("beer-stock/", include('stock.urls')),
    path('untappd/', include('untappd.urls')),
    path("sales/", include('sales.urls')),
]
