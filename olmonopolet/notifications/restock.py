from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from stores.models import Store

def send_restock_email(restock):
    '''
    Send email to users with overview of beers that have been restocked on their selected Vinmonopolet store  

    Parameters:  
    dict: Key is store and each store has a list of the beers that are restocked  

    Returns:  
    null

    '''


# TODO: Implement sending of email to users based on restock of beers in their preferred store. This requires a new model and app to store User store preferences.
# Currently notifications are sent to all users for all stores
    users = User.objects.all()


    for user in users:
        msg_context = {
            'username': user.username
            # 'store': 'Molde',
            # 'beers': restock[Store.objects.get(store_id=244)]
        }

        # TODO: Benytt related_name til å få tak i rating fra Untappd model
        # - Untappd Rating: {{ beer.untappd.all()[0].rating }}

        for key,value in restock.items():
            msg_context['store'] = key
            msg_context['beers'] = value

        rendered_msg = render_to_string('email/restock.html', msg_context)

        send_status = send_mail(f'Oppdatering varelager', 
                                '', 
                                'kjetil@olmonopolet.com', 
                                [user.email], 
                                fail_silently=False, 
                                html_message=rendered_msg)
        
        print(f"Sent email to: {user.email}") if send_status == 1 else print(f"Could not send email to: {user.email}")
