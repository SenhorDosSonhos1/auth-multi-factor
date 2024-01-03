from celery import shared_task
from hashlib import sha256
from django.core.mail import send_mail
from authentication.models import Token

@shared_task
def token_and_mail(user):
    try:
    # secret phrase
        secret  = sha256(('auth_multi_factor' + user.email).encode()).hexdigest()
        token = Token(user=user, token=secret)
        token.save()

        send_mail('CONFIRMAÇÃO DO E-MAIL', f'Ative a conta pelo link: http://127.0.0.1:8000/token/{token.token}', 'Marcelo Dev | Django', [f'{user.email}'])
        return True
    
    except Exception as e:
        return f'Erro:{e}'