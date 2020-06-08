from django.urls import path, include
from .views import StoreList

urlpatterns = [
    path('',StoreList.as_view()),
]
