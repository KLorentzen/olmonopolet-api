from django.shortcuts import render
from django.template.loader import render_to_string
from stock.models import BeerStock
from stores.models import Store
from beers.models import Beer
from django.views.generic import TemplateView

class AboutTemplateView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(store_id=self.kwargs['store_id'])
        return context
