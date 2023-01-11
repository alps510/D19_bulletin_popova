from datetime import time

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Profile


@shared_task()
def monday_post():

    recipient_list = User.objects.filter(profile__subscribe=True)
    recipient = []
    for e in recipient_list: recipient.append(e.email)
    html_content = render_to_string('account/email/weekly_post.html')
    msg = EmailMultiAlternatives(
        subject='Новости этой недели',
        body='',
        from_email='alps51@yandex.ru',
        to=recipient
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()




