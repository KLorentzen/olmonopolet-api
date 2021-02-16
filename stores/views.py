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

    # Check that query is not empty
    if request.POST["query"] != '':
        # Fetch all stores that math the query string
        stores = Store.objects.filter(name__icontains=request.POST["query"])
    return render(request, 'stubs/store_search.html', {'stores': stores})

# Regular Views
class StoreView(TemplateView):
    template_name='home.html'

# API Views
class StoreListAPIView(generics.ListAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer