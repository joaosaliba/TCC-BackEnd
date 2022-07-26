from django.shortcuts import render
from django.core.mail import send_mail
from urllib3 import HTTPResponse
from rede import settings
from django.template.loader import get_template

from django.core.mail import EmailMessage


def send(subject=None, message=None, recipient_list=['dimedat530@altpano.com']):
    print(settings.EMAIL_HOST_USER)
    print(subject)
    print(message)
    print(recipient_list)
    body = get_template("emailTemplate.html").render({
        'message': message})

    mail = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    mail.content_subtype = "html"

    return mail.send()
