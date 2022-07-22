from django.shortcuts import render
from django.core.mail import send_mail
from rede import settings


def send(self, subject=None, message=None, recipient_list=None):
    print(settings.EMAIL_HOST_USER)
    print(subject)
    print(message)
    print(recipient_list)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )
