from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store
from rest_framework import generics
from django.views.generic import TemplateView


# View Functions
def store_search(request):
    '''
    Used by search bar in landing page (home)
    '''
    # Returns no stores if query string is empty ('')
    stores = None

    # Check that store query is not empty
    if request.POST["query"] != '':
        # Trim leading/trailing whitespace from query string
        trimmed_query = request.POST["query"].strip()
        # Fetch all stores that match the query string
        stores = Store.objects.filter(active=True).filter(name__icontains=trimmed_query)
    return render(request, 'stubs/store_search.html', {'stores': stores, 'query': trimmed_query})

# Regular Views
class StoreView(TemplateView):
    template_name='home.html'

# API Views
class StoreListAPIView(generics.ListAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer