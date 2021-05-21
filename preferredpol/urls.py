from django.urls import path
from .views import pol_redirect

urlpatterns = [
    path('', pol_redirect, name='pol_redirect')
]