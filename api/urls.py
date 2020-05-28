from django.urls import path, include

urlpatterns = [
    path('beers/',include('beers.urls')),
    path("stores/", include('stores.urls')),
]
