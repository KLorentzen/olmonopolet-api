from django.urls import path, include
from .views import StoreView

urlpatterns = [
    path('', StoreView.as_view(), name='home')
]
