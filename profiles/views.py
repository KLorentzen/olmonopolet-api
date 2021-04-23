from django.shortcuts import render, redirect
from .models import Profile

# Create your views here.
def login_redirect(request):
    '''
    Redirect a User on successfull login.  
    1. Prefered Vinmonopolet Store associated with user  
    2. Home/Landing page  
    '''
    
    # Redirect to users preferred Vinmonopolet Store if defined
    try:
        profile = Profile.objects.get(user = request.user)

        return redirect('beer_stock', profile.store.store_id)

    except Exception:
        # Otherwise redirect to Home
        return redirect('home')

