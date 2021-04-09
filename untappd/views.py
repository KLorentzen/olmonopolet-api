from django.shortcuts import render
from rest_framework import generics
from .serializers import UntappdSerializer, UntappdMappingSerializer
from .models import Untappd, UntappdMapping
from olmonopolet.untappd_api import user

# View Functions
def sync_untappd_user(request):
    '''
    Syncronizes User check-ins at Untappd with Ølmonopolet
    '''
    beers_syncronized, sync_status, remaining_requests = user.sync_untappd(request.user)
    return render(request, 'stubs/sync_untappd_user.html', {'beers_syncronized': beers_syncronized, 'sync_status': sync_status, 'remaining_requests': remaining_requests})


# API Views
class UntappdList(generics.ListAPIView):
    queryset = Untappd.objects.all()
    serializer_class = UntappdSerializer

class UntappdDetail(generics.RetrieveAPIView):
    queryset = Untappd.objects.all()
    serializer_class = UntappdSerializer
    lookup_field = 'beer_id'

class MappingList(generics.ListAPIView):
    queryset = UntappdMapping.objects.filter(verified=True)
    serializer_class = UntappdMappingSerializer
    filterset_fields = ['beer_id']