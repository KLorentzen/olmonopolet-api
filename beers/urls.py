from django.urls import path, include
from .views import ReleaseListView, beer_release

urlpatterns = [
    path('release/', beer_release, name='beer_release'),
    path('<int:store_id>/release', ReleaseListView.as_view(), name='release_overview'),
]
