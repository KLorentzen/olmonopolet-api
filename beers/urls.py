from django.urls import path, include
from .views import BeerList

urlpatterns = [
    path('',BeerList.as_view()),

]
