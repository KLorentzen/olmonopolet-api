"""olmonopolet_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from olmonopolet_api import views

urlpatterns = [
    # Admin
    path('kjellaren/', admin.site.urls),

    # Auth
    path('profiles/',include('django.contrib.auth.urls')),
    path('profiles/',include('profiles.urls')),
    # Django Rest API
    # path('api/v1/',include('api.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('about/<int:store_id>/', views.AboutTemplateView.as_view(), name='about'),
    path('beers/', include('beers.urls')),
    path('stock/', include('stock.urls')),
    path('untappd/', include('untappd.urls')),
    path('', include('stores.urls')),
    #TODO: Add 404 for fallthrough paths
]
