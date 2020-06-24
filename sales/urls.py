from django.urls import path, include
from .views import DailySaleList

urlpatterns = [
    path('daily/',DailySaleList.as_view()),
]
