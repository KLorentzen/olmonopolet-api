from django.urls import path
from .views import login_redirect

urlpatterns = [
    path('login-redirect/', login_redirect, name='login_redirect'),

]
