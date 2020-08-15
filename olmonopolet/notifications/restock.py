from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from stores.models import Store
from notifications.models import EmailNotification

def send_restock_email(restock):
    '''
    Send email to users with overview of beers that have been restocked on their selected Vinmonopolet store  

    Parameters:  
    dict: Key is Store and each store has a list of the beers that are restocked  

    Returns:  
    null

    '''

    recipients = EmailNotification.objects.filter(store_updates=True)
    send_status = 0


    for recipient in recipients:
        msg_context = {
            'username': recipient.username.username,
            'store': recipient.store_id,
        }
        
        for key,value in restock.items():
            if key  == recipient.store_id: 
                msg_context['store'] = key 
                msg_context['beers'] = value
            

                rendered_msg = render_to_string('email/restock.html', msg_context)

                send_status = send_mail(f'Oppdatering varelager', 
                                        '', 
                                        'kjetil@olmonopolet.com', 
                                        [recipient.username.email], 
                                        fail_silently=False, 
                                        html_message=rendered_msg)
        
                print(f"Sent email to: {recipient.username.email}") if send_status == 1 else print(f"Could not send email to: {recipient.username.email}")

    return