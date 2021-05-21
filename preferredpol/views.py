from django.shortcuts import render, redirect
from profiles.models import Profile

# Create your views here.
def pol_redirect(request):
    '''
    Redirect a User to:
    a) preferred pol if logged in
    b) else to Home
    '''
    
    # Redirect to users preferred Vinmonopolet Store if defined
    try:
        profile = Profile.objects.get(user = request.user)

        return redirect('beer_stock', profile.store.store_id)

    except Exception:
        # Otherwise redirect to Home
        return redirect('home')

