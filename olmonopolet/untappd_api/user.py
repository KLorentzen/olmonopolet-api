import os, httpx 
from django.utils import timezone
from profiles.models import Profile
from untappd.models import UserCheckIn
from beers.models import Beer

def get_user_info(username):
    '''Retrieve info from Untappd for provided username.  

    Parameters:  
    arg1 str: Untappd username  
      
    Returns: 
    dict: JSON respons containing user information from Untappd
    int: remaining requests in current hour
    '''

    URL = f"https://api.untappd.com/v4/user/info/{username}"
    HEADERS = {"user-agent": f'Olmonopolet App({os.environ.get("UNTAPPD_CLIENT_ID")})' }
    PARAMS = {"client_id": os.environ.get('UNTAPPD_CLIENT_ID'),
              "client_secret": os.environ.get('UNTAPPD_CLIENT_SECRET')}
    
    try:
        response = httpx.get(URL, headers=HEADERS, params=PARAMS)

        user_info = response.json()
        ratelimit_remaining = int(response.headers['X-Ratelimit-Remaining'])

    except Exception as err:
        user_info = None
        ratelimit_remaining = 0

    return user_info, ratelimit_remaining

def get_user_beers(username, offset=0):
    '''Retrieve all beers checked in by Untappd username.  

    Parameters:  
    arg1 str: Untappd username  
      
    Returns:  
    dict: JSON respons containing user beer information from Untappd  
    int: remaining requests in current hour
    '''

    URL = f"https://api.untappd.com/v4/user/beers/{username}"
    HEADERS = {"user-agent": f'Olmonopolet App({os.environ.get("UNTAPPD_CLIENT_ID")})' }
    PARAMS = {"client_id": os.environ.get('UNTAPPD_CLIENT_ID'),
              "client_secret": os.environ.get('UNTAPPD_CLIENT_SECRET'),
              "limit": 50,
              "offset": offset}
    
    try:
        response = httpx.get(URL, headers=HEADERS, params=PARAMS)

        beer_info = response.json()
        ratelimit_remaining = int(response.headers['X-Ratelimit-Remaining'])

    except Exception as err:
        beer_info = None
        ratelimit_remaining = 0

    return beer_info, ratelimit_remaining

def sync_untappd(app_user):
    '''Syncronize Untappd check-ins for an Ølmonopolet User.  

    Parameters:  
    arg1 User: instance of User model 
      
    Returns:  
    list: All beers that are synced from Untappd  
    bool: syncronization status [True/False]  
    int: remaining requests in current hour based on Untappd Rate Limiting  
    '''

    # Untappd API has rateLimit=100
    MAX_REQUESTS = 100
    requests_remaining = MAX_REQUESTS
    untappd_page = 0

    synced_check_ins = []
    user_check_ins = 0

    # True if all user was syncronized successfully
    sync_status = True

    # Syncronize User Details from Untappd
    try:
        untappd_username = app_user.profiles.untappd_username

        untappd_user_info, requests_remaining = get_user_info(untappd_username)
        
        user_check_ins = untappd_user_info['response']['user']['stats']['total_beers']
        
        # Set number of requests to be made to Untappd in order to retrieve all check-ins
        # 50 beers per page/request
        quotient, remainder  = divmod(user_check_ins, 50) 
        if remainder != 0:
            total_pages = quotient + 1
        else:
            total_pages = quotient

        # Update User/Profile Avatar
        profile, created = Profile.objects.update_or_create(
            user = app_user,
            defaults = {
                'untappd_avatar_url': untappd_user_info['response']['user']['user_avatar']
            }
        )

        # Syncronize Untappd Check-Ins
        while untappd_page < total_pages and requests_remaining > 0:

            untappd_check_ins, requests_remaining = get_user_beers(untappd_username, untappd_page * 50)
            untappd_check_ins = untappd_check_ins['response']

            for beer in untappd_check_ins['beers']['items']:
                try:
                    # Iterate in case there are multiple Beers mapped to the same Untappd beer ID
                    # Example: Same beer but different size, 0,33L + 0,5L
                    for beer_mapping in Beer.objects.filter(mappings__untappd_id=beer['beer']['bid']):
                        check_in_obj, created = UserCheckIn.objects.get_or_create(
                                beer_id = beer_mapping,
                                user = app_user,
                                rating= beer['rating_score']
                            )
                        if created:
                            synced_check_ins.append(check_in_obj)

                except Exception as err:
                    # Exception occurs when user has checked in a Beer on Untappd that is not available on Vinmonopolet
                    pass

            untappd_page += 1

            # If Ratelimit is reached a syncronization is not complete
            if requests_remaining == 0:
                sync_status = False

    except Exception as err:
        sync_status = False


    if sync_status:
        profile, created = Profile.objects.update_or_create(
            user = app_user,
            defaults = {
                'untappd_sync_date': timezone.now()
            }
        )

    return synced_check_ins, sync_status, requests_remaining 
