from django.urls import path, include
from .views import BeerList, BeerDetail

urlpatterns = [
    path("<int:pk>/", BeerDetail.as_view()),
    path('',BeerList.as_view()),
]
