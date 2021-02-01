from django.urls import path, include
from .views import StoreListView

urlpatterns = [
    path('', StoreListView.as_view(), name='home')
]
