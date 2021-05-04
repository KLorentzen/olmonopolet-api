from django.urls import path, include
from .views import ReleaseListView, beer_release, OrderingRangeView, ordering_range_beers, ordering_range_search

urlpatterns = [
    path('release/', beer_release, name='beer_release'),
    path('<int:store_id>/release', ReleaseListView.as_view(), name='release_overview'),
    path('ordering-range/search', ordering_range_search, name='ordering_range_search'),
    path('ordering-range/all', ordering_range_beers, name='ordering_range_beers'),
    path('<int:store_id>/ordering-range/', OrderingRangeView.as_view(), name='ordering_range'),
]
