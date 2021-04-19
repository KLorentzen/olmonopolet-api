from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Beer
from stores.models import Store
from .serializers import BeerSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from django.utils import timezone

# Create your views here.

# View Functions
def beer_release(request):
    '''
    Return all beers which are to be released/launched in the future
    Paginated in order to use infinite scroll
    '''
    queryset = Beer.objects.filter(launch_date__gte=timezone.now()).order_by('launch_date', 'selection', 'name')
    paginator = Paginator(queryset, 50, 0)

    page_number = request.GET.get('page')
    beers = paginator.get_page(page_number)

    return render(request, 'stubs/beer_release.html', {'beers': beers})

# Regular Views
class ReleaseListView(TemplateView):
    template_name = "release.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        return context


# API Views
class BeerList(generics.ListAPIView):
    queryset=Beer.objects.all()
    serializer_class=BeerSerializer

class BeerDetail(generics.RetrieveAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
