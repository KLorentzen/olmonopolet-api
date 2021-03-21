from django.urls import path, include
from .views import StoreListAPIView

urlpatterns = [
    path('',StoreListAPIView.as_view()),
]
