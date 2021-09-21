from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


def send_token_for_user(request, user):
    token = default_token_generator.make_token(user)
    current_site = get_current_site(request)
    email = user.email
    send_mail(
        f'{current_site.domain} | Confirmation code',
        f'Confirmation code: {token}'
        f'{settings.EMAIL_FROM}@{current_site.domain}',
        [email],
        fail_silently=False,
    )
