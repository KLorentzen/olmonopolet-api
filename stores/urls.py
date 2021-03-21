from django.urls import path, include
from .views import StoreView, store_search

urlpatterns = [
    path('', StoreView.as_view(), name='home'),
    path('search/', store_search, name='store_search'),
]
