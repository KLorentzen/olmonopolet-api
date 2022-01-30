from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from stores.models import Store
from notifications.models import EmailNotification

def send_notification(subject, template):
    '''
    Send email to users   

    Parameters:  
    string: Subject  
    string: Name of template to use (include .html)  

    Returns:  
    null

    '''
    recipients = EmailNotification.objects.filter(store_updates=True).distinct('username')
    send_status = 0


    for recipient in recipients:
        msg_context = {
            'username': recipient.username.username,
        }
        

        rendered_msg = render_to_string(f'email/{template}', msg_context)

        send_status = send_mail(f'{subject}', 
                                '', 
                                'kjetil@olmonopolet.com', 
                                [recipient.username.email], 
                                fail_silently=False, 
                                html_message=rendered_msg)

        print(f"Sent email to: {recipient.username.email}") if send_status == 1 else print(f"Could not send email to: {recipient.username.email}")

    return